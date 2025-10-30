require 'synthesizer'

# Modular Synthesizer Class
class ModularSynth
  def initialize
    @oscillator = Synthesizer::Oscillator.new
    @filter = Synthesizer::Filter.new
    @envelope = Synthesizer::Envelope.new
    @mixer = Synthesizer::Mixer.new
  end

  # Play a note with modular routing
  def play(note, duration: 1.0, waveform: :sine, filter_freq: 1000, volume: 0.8)
    # Set up oscillator
    frequency = note_to_frequency(note)
    @oscillator.frequency = frequency
    @oscillator.waveform = waveform

    # Set up envelope
    @envelope.attack = 0.1
    @envelope.decay = 0.2
    @envelope.sustain = 0.7
    @envelope.release = 0.5

    # Set up filter
    @filter.cutoff_frequency = filter_freq
    @filter.resonance = 0.7

    # Connect modules
    signal = @oscillator.generate(duration)
    signal = @filter.process(signal)
    signal = @envelope.apply(signal)
    signal = @mixer.mix([signal], volumes: [volume])

    # Play the sound
    Synthesizer::Player.new.play(signal)
  end

  private

  # Note-to-frequency conversion
  def note_to_frequency(note)
    note_frequencies = {
      "C4" => 261.63, "D4" => 293.66, "E4" => 329.63, "F4" => 349.23,
      "G4" => 392.00, "A4" => 440.00, "B4" => 493.88,
      "C5" => 523.25, "D5" => 587.33, "E5" => 659.25
    }
    note_frequencies[note] || 440.0
  end
end

# Example Usage
synth = ModularSynth.new

# Play a simple melody
["C4", "E4", "G4", "C5"].each do |note|
  synth.play(note, duration: 0.5, waveform: :square, filter_freq: 800)
end

puts "Modular synthesizer melody played!"
