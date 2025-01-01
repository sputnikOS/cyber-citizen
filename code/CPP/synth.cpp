#include <iostream>
#include <cmath>
#include <PortAudio.h>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 512
#define NUM_CHANNELS 1
#define SAMPLE_TYPE float

// Frequency of A4 note (440 Hz)
#define A4_FREQUENCY 440.0

class MonoSynth {
public:
    MonoSynth() : frequency(A4_FREQUENCY), amplitude(0.5), waveform_type('s') {}

    // Set frequency
    void setFrequency(float freq) {
        frequency = freq;
    }

    // Set amplitude
    void setAmplitude(float amp) {
        amplitude = amp;
    }

    // Set waveform type ('s' for sine, 'q' for square, 'a' for sawtooth)
    void setWaveformType(char type) {
        waveform_type = type;
    }

    // Audio callback function to generate sound
    static int audioCallback(const void* inputBuffer, void* outputBuffer,
                             unsigned long framesPerBuffer,
                             const PaStreamCallbackTimeInfo* timeInfo,
                             PaStreamCallbackFlags statusFlags, void* userData) {
        MonoSynth* synth = static_cast<MonoSynth*>(userData);
        SAMPLE_TYPE* out = static_cast<SAMPLE_TYPE*>(outputBuffer);
        static float phase = 0.0;
        float phaseIncrement = 2.0 * M_PI * synth->frequency / SAMPLE_RATE;

        // Generate waveform
        for (unsigned long i = 0; i < framesPerBuffer; ++i) {
            float sample = 0.0;

            switch (synth->waveform_type) {
                case 's': // Sine wave
                    sample = synth->amplitude * sin(phase);
                    break;
                case 'q': // Square wave
                    sample = synth->amplitude * (sin(phase) > 0.0 ? 1.0 : -1.0);
                    break;
                case 'a': // Sawtooth wave
                    sample = synth->amplitude * (2.0 * (phase / (2.0 * M_PI)) - 1.0);
                    break;
                default:
                    sample = 0.0; // No sound for unknown waveforms
            }

            *out++ = sample;

            // Increment phase
            phase += phaseIncrement;
            if (phase >= 2.0 * M_PI) phase -= 2.0 * M_PI;
        }

        return paContinue;
    }

private:
    float frequency;
    float amplitude;
    char waveform_type;
};

int main() {
    PaError err;

    // Initialize PortAudio
    err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    MonoSynth synth;
    synth.setFrequency(A4_FREQUENCY); // Set frequency to A4 (440 Hz)
    synth.setAmplitude(0.5);           // Set amplitude to half
    synth.setWaveformType('s');       // Set to sine wave by default

    // Open the audio stream
    PaStream* stream;
    err = Pa_OpenDefaultStream(&stream,
                               NUM_CHANNELS,          // Mono output
                               NUM_CHANNELS,          // Mono input (not used here)
                               paFloat32,             // 32-bit float sample format
                               SAMPLE_RATE,           // Sample rate
                               FRAMES_PER_BUFFER,     // Buffer size
                               MonoSynth::audioCallback, // Callback function
                               &synth);               // Pass the synth object to callback
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    // Start the audio stream
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    // Let the sound play for a while
    std::cout << "Playing sound... Press Enter to stop." << std::endl;
    std::cin.get(); // Wait for user to press Enter

    // Stop and close the audio stream
    err = Pa_StopStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    // Terminate PortAudio
    Pa_Terminate();

    return 0;
}
