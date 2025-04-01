import abc
from enum import Enum
import pandas as pd
import numpy as np
import warnings
import datetime
import scipy.signal
from ..waveform import Waveform, LeqDurationMode, FrameBuilder
from .spectra import Spectrum, SpectrumByDigitalFilters, SpectrumByFFT
from .acoustic_weights import AcousticWeights
from ..audio_files.wavefile import WaveFile


class WeightingFunction(Enum):
    """
    This class provides the options on how to weight the calculation of the overall level values
    """

    unweighted = 0
    a_weighted = 1
    c_weighted = 2


class TimeHistory:
    """
    This class wraps the ability of the analysis to contain multiple spectrum objects and create a variation across
    time.

    Remarks
    2022-12-13 - FSM - added a function to collect the sound quality metrics from each of the spectra
    2022-12-13 - FSM - added a function to collect the times past midnight from the spectra objects
    """

    def __init__(self, a: Waveform = None, frames: FrameBuilder = None, integration_time: float = 0.25):
        from ..audio_files.ansi_standard_formatted_files import StandardBinaryFile
        """
        Constructor - this will build a class object for the TimeHistory and instantiate all properties and protected
        elements.

        Parameters
        ----------
        :param a: This is the waveform object that we want to process into a TimeHistory object
        :param integration_time: float - the size of the independent waveforms that will be processed into a series of
            Spectrum objects
        """

        self._spectra = None
        self._times = None
        self._waveform = a
        self._header = None

        #   Now if the Waveform object possesses a header field then we need to assign it to the header object here
        if self._waveform is not None:

            if frames is None:
                self._frame_builder = FrameBuilder(a, integration_time)
            else:
                self._frame_builder = frames
            self._integration_time = self._frame_builder.frame_length_seconds

            if isinstance(self.waveform, StandardBinaryFile):
                self._header = self.waveform.header
            elif isinstance(self.waveform, WaveFile):
                if self.waveform.header is not None:
                    self._header = self.waveform.header
            elif hasattr(self.waveform, 'header'):
                self._header = self.waveform.header
        else:
            self._integration_time = integration_time

    @abc.abstractmethod
    def _calculate_spectrogram(self):
        warnings.warn(
            "This function must be implemented in any child class to create the collection of spectra objects"
            " that define the time history"
        )
        pass

    def equivalent_level(
            self,
            weighting: WeightingFunction = WeightingFunction.a_weighted,
            equivalent_duration: float = 8 * 3600,
            start_sample: int = 0,
            stop_sample: int = None,
            leq_mode: LeqDurationMode = None,
            exposure_duration: float = None
    ):
        """
        This function computes the equivalent level on the spectral time history. If there is a weighting
        function specified this is applied to the spectra. Additionally, the duration of the summation
        is specified (in seconds) for the new value with a default of 8 hours. Finally, if there is a cause to exclude
        portions of the data (i.e. calculating the SEL for the 10 dB down points in community noise) you can specify
        the start and stop index. If the stop index is None, then the last pressure defines the limit of the summation.

        Parameters
        ----------
        weighting   :   WeightingFunction
            The enumeration to determine filtering function applied to the waveform
        equivalent_duration :   float
            The denominator of the energy averaging - in seconds - representing the desired length of total exposure
            time (e.g. an 8-hour duty day, or a 1-second sound exposure level)
        start_sample    :   int
            default = 0. The start sample of the pressure summation
        stop_sample :   int
            default = None. The stop sample, if the value is None, then it is replaced with the last sample index
        leq_mode    :   LeqDurationMode
            The enumeration to determine whether the input signal contains all energy
            of an exposure to the listener (transient) or the signal represents a sample of a longer-duration
            (steady_state) exposure
        exposure_duration   :   float
            If leq_mode is steady_state, this is the actual time of noise exposure to the
            listener in seconds

        """

        if stop_sample is None:
            stop_sample = len(self.times)

        number_of_samples = stop_sample - start_sample
        signal_duration = number_of_samples * np.mean(np.diff(self.times))

        weights = []
        if weighting == WeightingFunction.unweighted:
            weights = np.zeros(np.size(self.frequencies))
        elif weighting == WeightingFunction.a_weighted:
            weights = AcousticWeights.aw(self.frequencies)
        elif weighting == WeightingFunction.c_weighted:
            weights = AcousticWeights.cw(self.frequencies)

        spectrogram_array_decibels_weighted = self.spectrogram_array_decibels + \
                                              np.tile(weights, (len(self.times), 1))

        spectrogram_array_pascals_weighted = 10 ** (spectrogram_array_decibels_weighted / 20) * 20e-6

        s = np.sum(np.sum(spectrogram_array_pascals_weighted[start_sample:stop_sample, :] ** 2))

        total_energy_in_signal = s / self.time_history_sample_rate

        total_energy_of_exposure = []
        if leq_mode == LeqDurationMode.transient:
            total_energy_of_exposure = total_energy_in_signal
        elif leq_mode == LeqDurationMode.steady_state:
            if exposure_duration is None:
                exposure_duration = signal_duration
            total_energy_of_exposure = total_energy_in_signal * (exposure_duration / signal_duration)
        elif leq_mode is None:
            raise ValueError("User must specify a signal duration mode of class LeqDurationMode.")

        average_energy_over_equivalent_duration = total_energy_of_exposure / equivalent_duration

        return 10.0 * np.log10(average_energy_over_equivalent_duration / 20e-6 / 20e-6)

    def get_features(
            self, include_sq_metrics: bool = True, include_temporal_features: bool = True,
            include_spectral_features: bool = True, include_harmonic_features: bool = True,
            include_speech_features: bool = True
    ):
        """
        This function will obtain the temporal, spectral, sound quality, and level metrics from the waveform and the
        spectra within the time history.

        Parameters
        :param include_harmonic_features: bool
            Flag to determine whether to include the harmonic features in the output
        :param include_spectral_features: bool
            Flag to determine whether to include the spectral features in the output
        :param include_temporal_features: bool
            Flag to determine whether to include the temporal features in the output
        :param include_sq_metrics: bool
            Flag to determine whether to include the sound quality features in the output
        Returns
        -------
        A Pandas.DataFrame with the information from each spectrum
        """

        #   Create the DataFrame that will hold the data from the waveform and the spectrum objects
        names = ['time', 'lf', 'la', 'pnl']
        for f in self.frequencies:
            names.append('F{:06.0f}Hz'.format(f))

        timbre_feature_names = self.spectra[0].get_feature_names(
            include_sq_metrics=include_sq_metrics,
            include_harmonic_features=include_harmonic_features,
            include_spectral_features=include_spectral_features,
            include_temporal_features=include_temporal_features,
            include_speech_features=include_speech_features
        )
        for key in timbre_feature_names:
            names.append(key)

        df = pd.DataFrame(columns=names, index=np.arange(len(self.times)))

        for i in range(df.shape[0]):
            s = self.spectra[i]
            if isinstance(s, Spectrum):
                df.iloc[i, :4] = [s.time_past_midnight, s.overall_level, s.overall_a_weighted_level,
                                  s.perceived_noise_level]

                for band_index in range(len(self.frequencies)):
                    df.iloc[i, 4 + band_index] = s.pressures_decibels[band_index]

                n = 4 + len(self.frequencies)

                features = s.get_average_features(
                    include_sq_metrics=include_sq_metrics,
                    include_harmonic_features=include_harmonic_features,
                    include_spectral_features=include_spectral_features,
                    include_temporal_features=include_temporal_features,
                    include_speech_features=include_speech_features
                )
                for key in timbre_feature_names:
                    df.iloc[i, n] = features[key]

                    n += 1

        return df

    def save(self, filename: str):
        from ..audio_files.ansi_standard_formatted_files import StandardBinaryFile
        import datetime
        """
        This function saves the data from the waveform's header and the spectral information to a file 

        Parameters:
        -----------
        :param filename: string - the fill path to the output file
        
        Remarks
        -------
        20230221 - FSM - Updated the constructor to assign the header to the time history object if there is a header 
            within the Waveform object passed to the constructor.
        """

        #   open the output file

        file = open(filename, 'wt')

        #   If the header dictionary is present, write it to the output file

        if isinstance(self.waveform, StandardBinaryFile):
            header_dict = self.waveform.header
        elif isinstance(self.waveform, WaveFile):
            if self.waveform.header is not None:
                header_dict = self.waveform.header
        elif isinstance(self.header, dict):
            header_dict = self.header
            if 'HEADER SIZE' in header_dict.keys():
                del header_dict['HEADER SIZE']
        else:
            header_dict = None

        if header_dict is not None:
            header_line = ';{},{}\n'.format("HEADER SIZE", len(header_dict.keys()) + 1)
            file.write(header_line)

            unwanted_strs = [',']

            for key in header_dict.keys():
                for str in unwanted_strs:
                    new_key = key.replace(str, "_")
                header_line = ';{},{}\n'.format(new_key.upper(), header_dict[key])
                file.write(header_line)

        #   Now write the last header row which will have the time and frequency array

        header_line = ';{}'.format('year').ljust(7, ' ')
        header_line += ',{}'.format('month').ljust(7, ' ')
        header_line += ',{}'.format('day').ljust(7, ' ')
        header_line += ',{}'.format('hour').ljust(7, ' ')
        header_line += ',{}'.format('minute').ljust(7, ' ')
        header_line += ',{}'.format('second').ljust(7, ' ')

        for f in self.frequencies:
            header_line += ',{:6.2f}'.format(f).ljust(10, ' ')

        header_line += '\n'
        file.write(header_line)

        #   Now loop through the data
        for time_idx in range(len(self.spectra)):
            if isinstance(self.spectra[time_idx].time, datetime.datetime):
                data_line = '{:04.0f}'.format(self.spectra[time_idx].time.year).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.month).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.day).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.hour).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.minute).ljust(7, ' ')
                data_line += ',{:02.3f}'.format(
                    self.spectra[time_idx].time.second +
                    self.spectra[time_idx].time.microsecond * 1e-6
                ).ljust(7, ' ')
            else:
                hour = np.floor(self.spectra[time_idx].time / 3600)
                minute = np.floor((self.spectra[time_idx].time - hour * 3600) / 60)
                second = self.spectra[time_idx].time - 60 * (60 * hour + minute)

                data_line = '{:04.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(hour).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(minute).ljust(7, ' ')
                data_line += ',{:02.3f}'.format(second).ljust(7, ' ')

            #   Add the decibel data to the data_line object

            for j in range(len(self.frequencies)):
                data_line += ',{:03.2f}'.format(self.spectra[time_idx].pressures_decibels[j]).ljust(10, ' ')

            data_line += '\n'
            file.write(data_line)

        file.close()

    def trim(self, start_time=None, end_time=None, inplace: bool = False):
        """
        This function creates a subset of the existing data that is between the start_time and end_time objects. If the
        start_time is None then no elements are eliminated from the beginning; if the end_time is None then no elements
        are eliminated from the end.
        :param start_time:
            The start time of the subset. This can be either represented as a datetime object or a float. If the
            value is None, then the start time of the system is used.
        :param end_time:
            The stop time of the subset. This can be either represented as a datetime object or a float. If the
            value is None, then the stop time of the system is used.
        :param inplace:
            This parameter determines whether the data will be stored in the current object, loosing any values that
            were excluded based on the start_time and end_time. If True the data is lost, otherwise the subset is
            returned as a new object.
        """

        #   Determine the start of the subset
        if start_time is None:
            t0 = self.times_past_midnight[0]
        else:
            if isinstance(start_time, datetime.datetime):
                t0 = float(60 * (60 * start_time.hour + start_time.minute) + start_time.second) + float(
                    start_time.microsecond
                ) / 1e-6
            else:
                t0 = start_time

        #   Determine the end of the subset
        if end_time is None:
            t1 = self.times_past_midnight[-1]
        else:
            if isinstance(end_time, datetime.datetime):
                t1 = float(60 * (60 * end_time.hour + end_time.minute) + end_time.second) + float(
                    end_time.microsecond
                ) / 1e-6
            else:
                t1 = end_time

        #   obtain the indices for the subset based on the time past midnight estimation of the times
        idx = np.where((self.times_past_midnight >= t0) & (self.times_past_midnight <= t1))[0]

        #   Determine whether we will eliminate the data from this object or return a new object
        if inplace:
            self._times = self.times[idx]
            self._spectra = self.spectra[idx]
        else:
            spectra = TimeHistory()
            spectra._spectra = self.spectra[idx]
            spectra._times = self.times[idx]
            spectra._integration_time = np.mean(np.diff(spectra._times))
            spectra._header = self.header

            return spectra

    def interp(self, times: np.ndarray, inplace: bool = False):
        """
        In cases where the analysis times need to be adjusted, we want to determine the value of the sound pressure
        level spectra at a different set of times. This function will interpolate the values in the spectral levels
        and build a TimeHistory object at the specific times provided by the user.
        :param times:
            The times at which we want to calculate the spectral levels.
        :param inplace:
            This parameter determines whether the data will be stored in the current object, loosing any values not
            in the list of times provided, or return a new object.
        """

        #   Determine whether to use the datetime object or a floating point value
        use_float = False
        if isinstance(times[0], float):
            use_float = True

        #   Now gather the information into local variables that can be used in the interpolation
        spl = self.spectrogram_array_decibels
        if use_float:
            t = self.times_past_midnight
        else:
            t = self.times

        #   Create the sound pressure level object that will hold the output interpolated values
        ispl = np.zeros((len(times), spl.shape[1]), dtype=float)

        for freq_index in range(spl.shape[1]):
            ispl[:, freq_index] = np.interp(times, t, spl[:, freq_index])

        #   Determine whether to make a new object or modify the current object
        if inplace:
            pass
        else:
            spectra = TimeHistory()
            spectra._header = self.header
            spectra._spectra = np.empty((len(times),), dtype=Spectrum)
            for i in range(len(times)):
                spectra._spectra[i] = Spectrum()
                spectra._spectra[i]._frequencies = self.frequencies
                spectra._spectra[i]._acoustic_pressures_pascals = 20e-6 * 10 ** (spl / 20)
                spectra._spectra[i]._time0 = times[i]
            return spectra

    @staticmethod
    def load(filename: str):
        """
        This function will load the data from a file, and create the spectrum representation from the information within

        Parameters
        ----------

        filename: str - the full path to the
        """
        import os.path

        if not os.path.exists(filename):
            raise ValueError("The filename must exist")

        file = open(filename, "rt")
        contents = file.readlines()
        file.close()

        th = TimeHistory()

        if contents[0][0] == ';':
            th._header = dict()

            n = 0

            while contents[n][0] == ';' and not (contents[n][:5] == ";year"):
                #   Split the data apart based on the comma
                elements = contents[n].split(',')
                if len(elements) == 2:
                    th._header[elements[0][1:]] = elements[1][:-1]
                else:
                    value = elements[-1][:-1]
                    name = ','.join(elements[:-1])
                    th._header[name[1:]] = value

                #   increment the line
                n += 1

                if contents[n] == "\n":
                    n += 1

            elements = contents[n].split(',')
            f = list()
            for freq_index in range(6, len(elements)):
                f.append(float(elements[freq_index]))

            frequencies = np.asarray(f)
            n += 1

            th._spectra = np.empty((len(contents) - n,), dtype=Spectrum)

            for line_index in range(n, len(contents)):
                elements = contents[line_index].split(',')

                if int(elements[0]) == int(elements[1]) == int(elements[2]) == 0:
                    time = 60 * (60 * float(elements[3]) + float(elements[4])) + float(elements[5])
                else:
                    year = int(elements[0])
                    month = int(elements[1])
                    day = int(elements[2])
                    hour = int(elements[3])
                    minute = int(elements[4])
                    seconds = float(elements[5])
                    second = int(np.floor(seconds))
                    microsecond = int(np.floor(1e6 * (seconds - second)))
                    time = datetime.datetime(year, month, day, hour, minute, second, microsecond)

                spl = np.zeros((len(frequencies),))
                for spl_idx in range(6, len(elements)):
                    spl[spl_idx - 6] = float(elements[spl_idx])

                th._spectra[line_index - n] = Spectrum()
                th._spectra[line_index - n]._frequencies = frequencies
                th._spectra[line_index - n]._acoustic_pressures_pascals = 20e-6 * 10 ** (spl / 20)
                th._spectra[line_index - n]._time0 = time

            #   Set the integration time as the difference between the first and second times
            th._integration_time = th.times[1] - th.times[0]
            return th

    @property
    def waveform(self):
        if self._waveform is None:
            warnings.warn('No Waveform object has been passed to this TimeHistory object.')
        return self._waveform

    @property
    def signal(self):
        return self.waveform.samples

    @property
    def waveform_sample_rate(self):
        return self.waveform.sample_rate

    @property
    def time_history_sample_rate(self):
        """
        The number of samples per second of evey TimeHistory metric.
        """
        return 1.0 / self.integration_time

    @property
    def integration_time(self):
        return self._integration_time

    @property
    def duration(self):
        if self._waveform is not None:
            return self._waveform.duration
        else:
            return self.times[-1] - (self.times[0] - self.integration_time)

    @property
    def times(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        if self._times is None:
            if self.spectra[0].time_past_midnight is not None:
                t = np.zeros((len(self._spectra),), dtype=datetime.datetime)
            else:
                t = np.zeros((len(self._spectra),))

            for i in range(len(self.spectra)):
                if self.spectra[i]._waveform is not None:
                    t[i] = self.spectra[i].time
                else:
                    t[i] = self.spectra[i].time_past_midnight

            self._times = t

        return self._times

    @property
    def waveform_sample_size(self):
        return int(np.floor(self.integration_time * self._waveform.sample_rate))

    @property
    def frequencies(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        return self._spectra[0].frequencies

    @property
    def spectra(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        return self._spectra

    @property
    def spectrogram_array_decibels(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        spectrogram = np.zeros([len(self._spectra), len(self._spectra[0].frequencies)])
        for i in range(len(self._spectra)):
            spectrogram[i, :] = self._spectra[i].pressures_decibels

        return spectrogram

    @property
    def overall_level(self):
        """
        Overall sound pressure level, unweighted (i.e. flat wieghted, Z-weighted) time history.  Calculated as the
        energetic sum of the fractional octave band spectral time history.
        """
        if self.spectra is None:
            self._calculate_spectrogram()

        levels = np.zeros((len(self.times)), )

        for i in range(len(self.spectra)):
            levels[i] = self.spectra[i].overall_level

        return levels

    @property
    def overall_a_weighted_level(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        levels = np.zeros((len(self.times)), )

        for i in range(len(self.spectra)):
            levels[i] = self.spectra[i].overall_a_weighted_level

        return levels

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def roughness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        roughness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            roughness[i] = self.spectra[i].roughness

        return roughness

    @property
    def loudness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        loudness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            loudness[i] = self.spectra[i].loudness

        return loudness

    @property
    def sharpness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        sharpness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            sharpness[i] = self.spectra[i].sharpness

        return sharpness

    @property
    def spectral_centroid(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_centroid

        return r

    @property
    def spectral_spread(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_spread

        return r

    @property
    def spectral_skewness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_skewness

        return r

    @property
    def spectral_kurtosis(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_kurtosis

        return r

    @property
    def spectral_slope(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_slope

        return r

    @property
    def spectral_decrease(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_decrease

        return r

    @property
    def spectral_roll_off(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_roll_off

        return r

    @property
    def spectral_energy(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_energy

        return r

    @property
    def spectral_flatness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_flatness

        return r

    @property
    def spectral_crest(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_crest

        return r

    @property
    def fundamental_frequency(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].fundamental_frequency

        return r

    @property
    def times_past_midnight(self):
        tpm = np.zeros((len(self.spectra),))

        for i in range(len(tpm)):
            tpm[i] = self.spectra[i].time_past_midnight

        return tpm

    @staticmethod
    def from_data(levels, frequencies, times, levels_as_pressure: bool=False):
        """
        This function constructs the Spectrogram object from information obtained from the users and sets up an object
        that can be compared with external data without concern for differences in the methods to calculate the
        spectrogram data.

        :param levels: array-like - the 2-D levels with shape = [len(times), len(frequencies)]
        :param frequencies: array-like - the collection of frequencies that define one dimension of the levels matrix
        :param times: array-like - the collection of times within the spectrogram that define the second dimension
        :param levels_as_pressure: boolean - if True the levels matrix is assumed to be a pressure matrix,
        otherwise the levels are converted to a pressure matrix
        :returns: Spectrogram object
        """

        s = TimeHistory()
        s._spectra = np.empty((len(times),), dtype=Spectrum)

        if levels_as_pressure:
            p = levels
        else:
            p = 20e-6*10**(levels/20)

        for i in range(len(times)):
            spec = Spectrum()
            spec._time_past_midnight = times[i]
            spec._time0 = times[i]
            spec.frequencies = frequencies
            spec.pressures_pascals = p[i, :]

            s._spectra[i] = spec

        return s

    def concatenate(self, b=None, inplace: bool = False, normalize_time: bool = False):
        """
        This function will concatenate the TimeHistory that is passed as an argument to the current element. If the
        inplace argument is True, the data is concatenated to the current object, otherwise it is returned as a new
        object.

        Parameters
        ----------
        :param b: TimeHistory
            This is the object to concatenate with the current object
        :param inplace: bool
            Default = False - When False, this function will return a new TimeHistory Object, otherwise it returns a
            new TimeHistory object
        :param normalize_time: bool
            Default = False - This will normalize the time to a zero for the first spectra.
        """
        if not isinstance(b, TimeHistory):
            raise ValueError("The first argument is required to be a TimeHistory object.")
        if not np.array_equal(self.frequencies, b.frequencies):
            raise ValueError("Two TimeHistory objects must have same frequency content.")
        if np.round(self.integration_time, decimals=3) != np.round(b.integration_time, decimals=3):
            raise AttributeError("Two TimeHistory objects must have same integration time.")
        warnings.warn(
            'Concatenated TimeHistory object currently returns the header equal to the header of the first '
            'TimeHistory object only.'
        )

        if not inplace:
            #   Create the TimeHistory object without any data
            th = TimeHistory(integration_time=self.integration_time)
            th._header = self._header
            th._spectra = np.empty(len(self.times) + len(b.times), dtype=Spectrum)
            n = 0

            #   Loop through the current object and copy the contents of the spectra to the new object
            for i in range(len(self.times)):
                th._spectra[n] = self.spectra[i]
                if normalize_time:
                    th._spectra[n]._time0 = n * self._integration_time
                n += 1

            for i in range(len(b.times)):
                th._spectra[n] = b.spectra[i]
                if normalize_time:
                    th._spectra[n]._time0 = n * self._integration_time
                n += 1

            return th

        else:

            raise NotImplementedError("inplace concatenation not yet implemented.")

    def plot(
            self, xlabel: str = None, ylabel: str = None, ax=None, vmin: float = 0, vmax: float = 125,
            colormap: str = 'jet'
    ):
        """
        This will create a plot of the spectrogram on a 2-D plot. If the axis is provided in the ax object the image
        is added to the current figure, otherwise a new figure is created and the axis is returned.

        :param xlabel:
            The label for the x-axis of the chart. Defaults to "Time (sec)" if None
        :param ylabel:
            The label for the y-axis of the chart. Defaults to "Sound Pressure Level (dB)" if None
        :param ax:
            The axis that will hold the chart. A new axis is created if this argument is None.
        :param vmin:
            The minimum of the colorscale
        :param vmax:
            The maximum of the colorscale
        :param colormap:
            The color map to use in the coloring of the image
        :returns:
            The figure and axis if the ax argument is None, just the axis otherwise.
        """
        import matplotlib.pyplot as plt
        from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools as fob

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None
            ax.clear()

        plot = ax.pcolormesh(
            self.times_past_midnight - self.times_past_midnight[0],
            self.frequencies,
            self.spectrogram_array_decibels.transpose(),
            vmin=vmin,
            vmax=vmax,
            cmap=colormap,
            shading='gouraud'
        )

        ax.set_ylim([10, 10000])
        ax.set_yticks(fob.tob_frequencies_ansi())
        ax.set_yticklabels(fob.tob_frequencies_ansi())
        # ax.set_yscale('log')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return fig, ax

    def to_dataframe(self):
        """
        This function converts the information within the time history object into a Pandas.DataFrame
        :return: The data organized with the header as part of every row within a data frame
        :rtype: Pandas.DataFrame
        """
        #   Build the names of the columns for the DataFrame
        names = list(self.header.keys())
        names.append('tpm')
        names.append('lf')
        names.append('la')
        for f in self.frequencies:
            names.append('F{:05.0f}Hz'.format(f))

        dataset = pd.DataFrame(columns=names, index=np.arange(len(self.times)))
        i = len(self.header)
        dataset.iloc[:, i] = self.times_past_midnight
        dataset.iloc[:, i + 1] = self.overall_level
        dataset.iloc[:, i + 2] = self.overall_a_weighted_level
        dataset.iloc[:, i+3:] = self.spectrogram_array_decibels

        for key in self.header.keys():
            dataset[key] = self.header[key]

        return dataset


class NarrowbandTimeHistory(TimeHistory):
    """
    This class implements the _calculate_spectrogram function using the Narrowband_Spectrum class
    """

    def __init__(self, a: Waveform, frames: FrameBuilder = None, integration_time: float = 0.25, fft_size: int = None):
        if frames is None:
            frames = FrameBuilder(a, frame_width_sec=integration_time)
        super().__init__(a, frames)

        self._fft_size = fft_size

        #   There is no default value for the FFT size, so let's do some analysis to determine what the most optimal
        #   value of this should be if it is not provided.
        if self._fft_size is None:

            #   Set the default block size
            sub_wfm_length = self._frame_builder.frame_length_samples
            self._fft_size = int(2 ** np.floor(np.log2(sub_wfm_length)))

        elif (self._fft_size > len(self.waveform.samples)) or \
                (self.fft_size > self._frame_builder.frame_length_samples):
            raise ValueError('FFT block size cannot be greater than the total length of the signal.')

    @property
    def fft_size(self):
        return self._fft_size

    def _calculate_spectrogram(self):
        from ..waveform import TrimmingMethods

        """
        This function will divide the waveform up into contiguous sections of the waveform
        """

        #   Determine the maximum number of whole samples that exist within the waveform.
        N = self._frame_builder.complete_frame_count

        #   Create the list of spectra that will be used later
        self._spectra = np.empty((N,), dtype=SpectrumByFFT)

        #   Set the starting sample
        s0 = 0

        #   Loop through the elements and create the spectral object
        for n in range(N):
            #   get the subset of data from the waveform
            subset = self._frame_builder.get_next_waveform_subset()

            #   Create the spectrum object and add it as the ith element in the array
            self._spectra[n] = SpectrumByFFT(subset, self.fft_size)

            #   increment the starting sample
            s0 += self.waveform_sample_size

    def to_logarithmic_band_time_history(self, fob_band_width: int = 3, f0: float = 10, f1: float = 10000):
        """
        This function utilizes the functions within the SpectrumByFFT to generate a collection of
        Spectrum objects within a TimeHistory object.

        Parameters
        ----------
        fob_band_width: int, Default = 3 - the fractional octave bandwidth
        f0: float, default = 10 - the lower frequency band center frequency
        f1: float, default = 10000 - the upper frequency band center frequency

        Returns
        -------
        A TimeHistory object with the information from this time history converted to a different frequency
        representation.
        """

        #   Create the output object
        th = TimeHistory()
        th.header = self.header
        th._spectra = np.empty(len(self.spectra), dtype=Spectrum)

        for i in range(len(self.spectra)):
            if isinstance(self.spectra[i], SpectrumByFFT):
                th._spectra[i] = self.spectra[i].to_fractional_octave_band(fob_band_width, f0, f1)
                if not th._spectra[i].acoustic_pressures_pascals.any():
                    warnings.warn("Creating the logarithmic band time history has result in a spectrum (at index {}) with acoustic_pressures of 0. Consider if this is desired.".format(i))

        return th


class LogarithmicBandTimeHistory(TimeHistory):
    """
    This function possesses the digital filtered version of the spectrum
    """

    def __init__(
            self, a: Waveform, frames: FrameBuilder = None, integration_time: float = 0.25,
            fob_band_width: int = 3, f0: float = 10, f1: float = 10000):
        if frames is None:
            frames = FrameBuilder(a, frame_width_sec=integration_time)

        super().__init__(a, frames)

        self._bandwidth = fob_band_width
        self._start_frequency = f0
        self._stop_frequency = f1

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def start_frequency(self):
        return self._start_frequency

    @property
    def stop_frequency(self):
        return self._stop_frequency

    @property
    def settle_time(self):
        return self.settle_samples / self.waveform.sample_rate

    @property
    def settle_samples(self):
        """
        Based on requirements of Matlab filtering, you must have at least 3 times the number of coefficients to
        accurately filter data. So this will start with that minimum, and then move through the full octave frequency
        band numbers to determine the minimum number of samples that are required for the filter to adequately settle.
        """

        return self.spectra[0].settle_samples

    def _calculate_spectrogram(self):

        """
        This function will divide the waveform up into contiguous sections of the waveform
        """

        #   Determine the maximum number of whole samples that exist within the waveform.
        N = self._frame_builder.complete_frame_count

        #   Create the list of spectra that will be used later
        self._spectra = np.empty((N,), dtype=SpectrumByDigitalFilters)

        #   Set the starting sample
        s0 = 0

        #   Loop through the elements and create the spectral object
        for n in range(N):
            #   get the subset of data from the waveform
            subset = self._frame_builder.get_next_waveform_subset(self.waveform)

            #   Create the spectrum object and add it as the ith element in the array
            self._spectra[n] = SpectrumByDigitalFilters(
                subset, self.bandwidth,
                self.start_frequency,
                self.stop_frequency
            )

            #   increment the starting sample
            s0 += self.waveform_sample_size

    def calculate_engineering_scale_factor(self, calibration_level: float = 94, calibration_frequency=1000):
        sensitivities = np.zeros((len(self.spectra),))

        for i in range(len(self.spectra)):
            sensitivities[i] = self.spectra[i].calculate_engineering_unit_scale_factor(
                calibration_level,
                calibration_frequency
            )

        return np.mean(sensitivities)


class Spectrogram(NarrowbandTimeHistory):
    """
    This class is meant to utilize the spectrogram function within scipy.signal to generate the spectral values, but
    employ the representations of the spectra within PyTimbre to hold the data.
    """

    def __init__(self, a: Waveform = None, fft_size: int = 4096):
        """
        This builds the representation of the class, utilizing the parent class for the creation of the protected
        members.

        :param a:
            The waveform that will be processed with the spectrogram function
        :param integration_time:
            The desired time window that will be used for the time history. If the value is None, then the default of
            the spectrogram is used instead.
        :param fft_size:
            This is the number fo frequency bins in the double-sided frequency trace
        """

        super().__init__(a, None, fft_size=fft_size)

    def _calculate_spectrogram(self):
        """
        This function uses the internal representation of the waveform to determine the sampling methods used for the
        creation of the spectral varying time history.
        """
        import scipy.signal
        import scipy.signal.windows

        #   Use the spectrogram function to create the acoustic levels
        f, t, sxx = scipy.signal.spectrogram(
            self.waveform.samples,
            self.waveform.sample_rate,
            window=scipy.signal.windows.tukey(self.fft_size, 0.25),
            nperseg=self.fft_size,
            noverlap=self.fft_size / 2,
            nfft=self.fft_size,
            return_onesided=True,
            scaling='spectrum',
            mode='magnitude'
        )

        self._integration_time = np.mean(np.diff(t))

        #   Create the array of spectrum objects that we will insert the information into
        self._spectra = np.empty((len(t),), dtype=Spectrum)

        #   Loop through the information and insert the data into the array
        for i in range(len(t)):
            self._spectra[i] = Spectrum()

            self._spectra[i].frequencies = f
            self._spectra[i]._time0 = t[i]
            self._spectra[i]._acoustic_pressures_pascals = np.sqrt(sxx[:, i])


