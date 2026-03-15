#pragma once
#include <JuceHeader.h>
#include "PluginProcessor.h"

class RemixBuddyAudioProcessorEditor : public juce::AudioProcessorEditor, 
                                        public juce::FileDragAndDropTarget,
                                        private juce::Timer {
public:
    enum class UIState {
        Idle,
        CheckingService,
        ServiceAvailable,
        ServiceUnavailable,
        SubmittingJob,
        PollingJob,
        Completed,
        Failed
    };

    RemixBuddyAudioProcessorEditor (RemixBuddyAudioProcessor&);
    ~RemixBuddyAudioProcessorEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    bool isInterestedInFileDrag (const juce::StringArray& files) override;
    void filesDropped (const juce::StringArray& files, int x, int y) override;

private:
    void timerCallback() override;
    void setUIState (UIState newState);
    void updateDebugInfo();
    void startAnalysis();

    RemixBuddyAudioProcessor& audioProcessor;
    UIState currentState = UIState::Idle;
    
    juce::Label titleLabel { "title", "RemixBuddy v0.2a" };
    juce::Label dropZoneLabel { "dropZone", "Drop Audio File Here" };
    juce::TextButton analyzeButton { "Analyze" };
    juce::Label statusLabel { "status", "Status: Idle" };
    juce::ProgressBar progressBar;
    juce::Label resultLabel { "results", "-" };
    
    // Debug Info
    juce::Label debugLabel { "debug", "Last API: -\nStatus: -\nError: -" };

    juce::File selectedFile;
    juce::String currentJobId;
    double progressValue = 0.0;
    int healthCheckCounter = 0;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (RemixBuddyAudioProcessorEditor)
};
