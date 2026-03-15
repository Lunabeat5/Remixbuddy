#include "ServiceConnector.h"

namespace RemixBuddy {

ServiceConnector::ServiceConnector() {}

juce::var ServiceConnector::performRequest(const juce::String& endpoint, 
                                          const juce::String& method, 
                                          const juce::String& jsonBody) 
{
    lastResponse.endpoint = endpoint;
    lastResponse.statusCode = 0;
    lastResponse.errorMessage = "";
    lastResponse.rawBody = "";

    juce::URL url(baseUrl + endpoint);
    
    // Construct options in a single chain to avoid immutable assignment errors
    auto options = juce::URL::InputStreamOptions(juce::URL::ParameterHandling::inAddress)
                    .withConnectionTimeoutMs(2000);

    if (method == "POST") {
        url = url.withPOSTData(jsonBody);
        // We create a NEW options object because of immutability
        auto postOptions = options.withExtraHeaders("Content-Type: application/json\nAccept: application/json");
        
        auto stream = url.createInputStream(postOptions);
        if (stream != nullptr) {
            if (auto* webStream = dynamic_cast<juce::WebInputStream*>(stream.get())) {
                lastResponse.statusCode = webStream->getStatusCode();
            }
            lastResponse.rawBody = stream->readEntireStreamAsString();
            auto parseResult = juce::JSON::parse(lastResponse.rawBody);
            if (!parseResult.isUndefined()) {
                if (lastResponse.statusCode >= 200 && lastResponse.statusCode < 300) {
                    currentStatus = ServiceStatus::Available;
                    return parseResult;
                }
                lastResponse.errorMessage = "Server error " + juce::String(lastResponse.statusCode);
                return juce::var();
            }
            lastResponse.errorMessage = "JSON Parse Error";
            return juce::var();
        }
    } else {
        auto stream = url.createInputStream(options);
        if (stream != nullptr) {
            if (auto* webStream = dynamic_cast<juce::WebInputStream*>(stream.get())) {
                lastResponse.statusCode = webStream->getStatusCode();
            }
            lastResponse.rawBody = stream->readEntireStreamAsString();
            auto parseResult = juce::JSON::parse(lastResponse.rawBody);
            if (!parseResult.isUndefined()) {
                if (lastResponse.statusCode >= 200 && lastResponse.statusCode < 300) {
                    currentStatus = ServiceStatus::Available;
                    return parseResult;
                }
                lastResponse.errorMessage = "Server error " + juce::String(lastResponse.statusCode);
                return juce::var();
            }
            lastResponse.errorMessage = "JSON Parse Error";
            return juce::var();
        }
    }

    currentStatus = ServiceStatus::Unavailable;
    lastResponse.errorMessage = "Connection failed / Timeout";
    return juce::var();
}

ServiceConnector::ServiceStatus ServiceConnector::checkHealth() {
    auto response = performRequest("/health", "GET");
    if (response.isObject() && response.getProperty("status", "").toString() == "ok") {
        currentStatus = ServiceStatus::Available;
    } else {
        currentStatus = ServiceStatus::Unavailable;
    }
    return currentStatus;
}

juce::String ServiceConnector::submitAnalysis(const juce::File& file) {
    juce::DynamicObject::Ptr body = new juce::DynamicObject();
    body->setProperty("request_id", juce::Uuid().toString());
    body->setProperty("file_path", file.getFullPathName());
    body->setProperty("detect_sections", true);
    body->setProperty("detect_key", true);
    body->setProperty("detect_bpm", true);

    auto response = performRequest("/jobs/analyze", "POST", juce::JSON::toString(juce::var(body)));
    
    if (response.isObject() && response.hasProperty("job_id")) {
        return response.getProperty("job_id", "").toString();
    }
    return "";
}

ServiceConnector::JobStatus ServiceConnector::getJobStatus(const juce::String& jobId) {
    auto response = performRequest("/jobs/" + jobId, "GET");
    JobStatus status;
    status.jobId = jobId;

    if (response.isObject()) {
        status.status = response.getProperty("status", "unknown").toString();
        status.progress = (float)response.getProperty("progress", 0.0);
        status.message = response.getProperty("message", "").toString();
        status.valid = true;
    }
    return status;
}

ServiceConnector::AnalysisResult ServiceConnector::getAnalysisResult(const juce::String& jobId) {
    auto response = performRequest("/jobs/" + jobId + "/result", "GET");
    AnalysisResult result;

    if (response.isObject()) {
        result.bpm = (float)response.getProperty("bpm", 0.0);
        result.key = response.getProperty("key", "").toString();
        result.duration = (double)response.getProperty("duration_sec", 0.0);
        result.success = true;
    }
    return result;
}

} // namespace RemixBuddy
