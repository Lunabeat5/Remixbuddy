cmake_minimum_required(VERSION 3.22)

project(RemixBuddy VERSION 0.2.0 LANGUAGES CXX)

# --- JUCE Setup ---
add_subdirectory(../libs/JUCE libs/JUCE)

# --- Plugin Target ---
juce_add_plugin(RemixBuddy
    COMPANY_NAME "ASDZ"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS TRUE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_CODE ASDZ
    PLUGIN_CODE RMXB
    FORMATS VST3
    PRODUCT_NAME "RemixBuddy"
    VST2_ID RMXB
    VST3_CAN_REPLACE_VST2 FALSE
)

juce_generate_juce_header(RemixBuddy)

# --- Source Files ---
target_sources(RemixBuddy PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginProcessor.h
    Source/PluginEditor.cpp
    Source/PluginEditor.h
    Source/ServiceConnector.cpp
    Source/ServiceConnector.h
)

# --- Compiler & Linker Settings ---
target_compile_features(RemixBuddy PRIVATE cxx_std_17)

target_link_libraries(RemixBuddy PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_gui_extra
    juce::juce_core
    juce::juce_events
    juce::juce_graphics
    juce::juce_data_structures
)

target_compile_definitions(RemixBuddy PRIVATE
    JUCE_VST3_CAN_REPLACE_VST2=0
)

# --- Binary Location ---
set_target_properties(RemixBuddy PROPERTIES
    JUCE_VST3_DESTINATION "C:/Program Files/Common Files/VST3"
)
