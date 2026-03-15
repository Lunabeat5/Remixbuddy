#include "PluginProcessor.h"
#include "PluginEditor.h"

RemixBuddyAudioProcessor::RemixBuddyAudioProcessor()
    : AudioProcessor (BusesProperties().withInput ("Input", juce::AudioChannelSet::stereo(), true)
                                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true))
{}

RemixBuddyAudioProcessor::~RemixBuddyAudioProcessor() {}

void RemixBuddyAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock) {}
void RemixBuddyAudioProcessor::releaseResources() {}

bool RemixBuddyAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const {
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;
    return true;
}

void RemixBuddyAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages) {
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();

    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, buffer.getNumSamples());
}

juce::AudioProcessorEditor* RemixBuddyAudioProcessor::createEditor() {
    return new RemixBuddyAudioProcessorEditor (*this);
}

// This creates new instances of the plugin
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter() {
    return new RemixBuddyAudioProcessor();
}
