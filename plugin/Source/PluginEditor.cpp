#include "PluginProcessor.h"
#include "PluginEditor.h"

RemixBuddyAudioProcessorEditor::RemixBuddyAudioProcessorEditor (RemixBuddyAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p), progressBar (progressValue)
{
    setSize (450, 450);

    titleLabel.setFont (juce::Font (20.0f, juce::Font::bold));
    addAndMakeVisible (titleLabel);

    dropZoneLabel.setColour (juce::Label::backgroundColourId, juce::Colours::black.withAlpha (0.2f));
    dropZoneLabel.setJustificationType (juce::Justification::centred);
    addAndMakeVisible (dropZoneLabel);

    analyzeButton.onClick = [this] { startAnalysis(); };
    addAndMakeVisible (analyzeButton);

    statusLabel.setJustificationType (juce::Justification::centred);
    addAndMakeVisible (statusLabel);

    addAndMakeVisible (progressBar);

    resultLabel.setJustificationType (juce::Justification::centred);
    addAndMakeVisible (resultLabel);

    debugLabel.setFont (juce::Font (12.0f));
    debugLabel.setColour (juce::Label::textColourId, juce::Colours::grey);
    addAndMakeVisible (debugLabel);

    setUIState (UIState::CheckingService);
    startTimer (1000); // UI & Health timer
}

RemixBuddyAudioProcessorEditor::~RemixBuddyAudioProcessorEditor() {
    stopTimer();
}

void RemixBuddyAudioProcessorEditor::paint (juce::Graphics& g) {
    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));
}

void RemixBuddyAudioProcessorEditor::resized() {
    auto area = getLocalBounds().reduced (20);
    titleLabel.setBounds (area.removeFromTop (40));
    area.removeFromTop (10);
    dropZoneLabel.setBounds (area.removeFromTop (80));
    area.removeFromTop (10);
    analyzeButton.setBounds (area.removeFromTop (40).withSizeKeepingCentre (140, 40));
    area.removeFromTop (10);
    statusLabel.setBounds (area.removeFromTop (25));
    progressBar.setBounds (area.removeFromTop (15));
    area.removeFromTop (10);
    resultLabel.setBounds (area.removeFromTop (60));
    debugLabel.setBounds (area);
}

void RemixBuddyAudioProcessorEditor::setUIState (UIState newState) {
    currentState = newState;
    
    switch (currentState) {
        case UIState::Idle:
            statusLabel.setText ("Ready", juce::dontSendNotification);
            analyzeButton.setEnabled (selectedFile.exists());
            break;
        case UIState::CheckingService:
            statusLabel.setText ("Checking Service...", juce::dontSendNotification);
            analyzeButton.setEnabled (false);
            break;
        case UIState::ServiceAvailable:
            statusLabel.setText ("Service Online", juce::dontSendNotification);
            analyzeButton.setEnabled (selectedFile.exists());
            break;
        case UIState::ServiceUnavailable:
            statusLabel.setText ("Service Offline", juce::dontSendNotification);
            analyzeButton.setEnabled (false);
            break;
        case UIState::SubmittingJob:
            statusLabel.setText ("Submitting...", juce::dontSendNotification);
            analyzeButton.setEnabled (false);
            break;
        case UIState::PollingJob:
            statusLabel.setText ("Processing...", juce::dontSendNotification);
            analyzeButton.setEnabled (false);
            break;
        case UIState::Completed:
            statusLabel.setText ("Analysis Complete", juce::dontSendNotification);
            analyzeButton.setEnabled (true);
            break;
        case UIState::Failed:
            statusLabel.setText ("Analysis Failed", juce::dontSendNotification);
            analyzeButton.setEnabled (true);
            break;
    }
    updateDebugInfo();
}

void RemixBuddyAudioProcessorEditor::updateDebugInfo() {
    auto last = audioProcessor.getServiceConnector().getLastResponse();
    juce::String debugText = "Endpoint: " + last.endpoint + 
                             "\nStatus: " + juce::String(last.statusCode) + 
                             "\nError: " + last.errorMessage;
    debugLabel.setText (debugText, juce::dontSendNotification);
}

bool RemixBuddyAudioProcessorEditor::isInterestedInFileDrag (const juce::StringArray& files) {
    return files[0].endsWith (".wav") || files[0].endsWith (".mp3");
}

void RemixBuddyAudioProcessorEditor::filesDropped (const juce::StringArray& files, int x, int y) {
    selectedFile = juce::File (files[0]);
    dropZoneLabel.setText ("File: " + selectedFile.getFileName(), juce::dontSendNotification);
    if (currentState == UIState::ServiceAvailable || currentState == UIState::Idle) {
        setUIState (UIState::Idle);
    }
}

void RemixBuddyAudioProcessorEditor::startAnalysis() {
    setUIState (UIState::SubmittingJob);
    currentJobId = audioProcessor.getServiceConnector().submitAnalysis (selectedFile);
    
    if (currentJobId.isNotEmpty()) {
        setUIState (UIState::PollingJob);
    } else {
        setUIState (UIState::Failed);
    }
}

void RemixBuddyAudioProcessorEditor::timerCallback() {
    healthCheckCounter++;

    // Periodic Health Check (every 5 seconds)
    if (currentState != UIState::PollingJob && healthCheckCounter >= 5) {
        healthCheckCounter = 0;
        auto status = audioProcessor.getServiceConnector().checkHealth();
        if (status == RemixBuddy::ServiceConnector::ServiceStatus::Available) {
            if (currentState == UIState::ServiceUnavailable || currentState == UIState::CheckingService)
                setUIState (UIState::ServiceAvailable);
        } else {
            setUIState (UIState::ServiceUnavailable);
        }
    }

    // Job Polling
    if (currentState == UIState::PollingJob) {
        auto job = audioProcessor.getServiceConnector().getJobStatus (currentJobId);
        progressValue = job.progress;
        statusLabel.setText ("Processing: " + job.message, juce::dontSendNotification);

        if (job.status == "completed") {
            auto result = audioProcessor.getServiceConnector().getAnalysisResult (currentJobId);
            if (result.success) {
                resultLabel.setText ("BPM: " + juce::String (result.bpm, 2) + 
                                     " | Key: " + result.key + 
                                     " | Duration: " + juce::String (result.duration, 1) + "s", 
                                     juce::dontSendNotification);
                setUIState (UIState::Completed);
            } else {
                setUIState (UIState::Failed);
            }
        } else if (job.status == "failed" || !job.valid) {
            setUIState (UIState::Failed);
        }
    }
    
    updateDebugInfo();
}
