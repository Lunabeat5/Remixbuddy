#pragma once
#include <JuceHeader.h>

namespace RemixBuddy {

class ServiceConnector {
public:
    enum class ServiceStatus {
        Unknown,
        Available,
        Unavailable,
        Error
    };

    struct LastResponseInfo {
        juce::String endpoint;
        int statusCode = 0;
        juce::String errorMessage;
        juce::String rawBody;
    };

    struct AnalysisResult {
        float bpm = 0.0f;
        juce::String key;
        double duration = 0.0;
        bool success = false;
    };

    struct JobStatus {
        juce::String jobId;
        juce::String status;
        float progress = 0.0f;
        juce::String message;
        bool valid = false;
    };

    struct StemAssets {
        bool ready = false;
        juce::String statusMessage;
        juce::String outputDirectory;
        juce::StringArray stems;
    };

    ServiceConnector();
    ~ServiceConnector() = default;

    /** Submits a file for analysis. Returns the jobId. */
    juce::String submitAnalysis(const juce::File& file);

    /** Submits a file for stem separation via Demucs. */
    juce::String submitStemJob(const juce::File& file);

    /** Polls the status of a job. */
    JobStatus getJobStatus(const juce::String& jobId);

    /** Gets the final result. */
    AnalysisResult getAnalysisResult(const juce::String& jobId);

    /** Retrieves stem assets once separation completes. */
    StemAssets getStemAssets(const juce::String& jobId);

    /** Checks if the service is healthy. Updates internal status. */
    ServiceStatus checkHealth();

    ServiceStatus getStatus() const { return currentStatus; }
    const LastResponseInfo& getLastResponse() const { return lastResponse; }

private:
    juce::String baseUrl = "http://127.0.0.1:17845";
    ServiceStatus currentStatus = ServiceStatus::Unknown;
    LastResponseInfo lastResponse;

    juce::var performRequest(const juce::String& endpoint, 
                             const juce::String& method, 
                             const juce::String& jsonBody = "");
};

} // namespace RemixBuddy
