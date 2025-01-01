// Include necessary headers for a VST plugin
#include <cmath>
#include <cstring>

#include "audioeffectx.h"
#include "vstgui.h"

class NeveChannelStrip : public AudioEffectX {
public:
    NeveChannelStrip(audioMasterCallback audioMaster);
    ~NeveChannelStrip();

    void processReplacing(float** inputs, float** outputs, VstInt32 sampleFrames) override;
    void setParameter(VstInt32 index, float value) override;
    float getParameter(VstInt32 index) override;
    void getParameterName(VstInt32 index, char* label) override;
    void getParameterDisplay(VstInt32 index, char* text) override;
    void getParameterLabel(VstInt32 index, char* label) override;

private:
    enum Parameters {
        GAIN,
        EQ_LOW,
        EQ_MID,
        EQ_HIGH,
        SATURATION,
        COMP_THRESHOLD,
        COMP_RATIO,
        NUM_PARAMS
    };

    float parameters[NUM_PARAMS];
    float gain;
    float eqLow;
    float eqMid;
    float eqHigh;
    float saturation;
    float compThreshold;
    float compRatio;

    float applySaturation(float sample);
    float applyEQ(float sample, float low, float mid, float high);
};

// Constructor
NeveChannelStrip::NeveChannelStrip(audioMasterCallback audioMaster) : AudioEffectX(audioMaster, 1, NUM_PARAMS) {
    setNumInputs(2);    // stereo input
    setNumOutputs(2);   // stereo output
    setUniqueID('NChS');
    canProcessReplacing();

    // Initialize parameters
    parameters[GAIN] = 0.5f; // Neutral gain
    parameters[EQ_LOW] = 0.5f;
    parameters[EQ_MID] = 0.5f;
    parameters[EQ_HIGH] = 0.5f;
    parameters[SATURATION] = 0.5f;
    parameters[COMP_THRESHOLD] = 0.5f;
    parameters[COMP_RATIO] = 0.5f;

    gain = 1.0f;
    eqLow = eqMid = eqHigh = 1.0f;
    saturation = 0.0f;
    compThreshold = 0.0f;
    compRatio = 1.0f;
}

// Destructor
NeveChannelStrip::~NeveChannelStrip() {}

void NeveChannelStrip::processReplacing(float** inputs, float** outputs, VstInt32 sampleFrames) {
    float* in1 = inputs[0];
    float* in2 = inputs[1];
    float* out1 = outputs[0];
    float* out2 = outputs[1];

    for (VstInt32 i = 0; i < sampleFrames; ++i) {
        // Gain stage
        float sampleL = in1[i] * gain;
        float sampleR = in2[i] * gain;

        // Apply saturation (Neve console characteristic)
        sampleL = applySaturation(sampleL);
        sampleR = applySaturation(sampleR);

        // EQ stage (emulating Neve EQ curves)
        sampleL = applyEQ(sampleL, eqLow, eqMid, eqHigh);
        sampleR = applyEQ(sampleR, eqLow, eqMid, eqHigh);

        // Compression stage (simple hard-knee compression)
        if (fabs(sampleL) > compThreshold) {
            sampleL = compThreshold + (sampleL - compThreshold) / compRatio;
        }
        if (fabs(sampleR) > compThreshold) {
            sampleR = compThreshold + (sampleR - compThreshold) / compRatio;
        }

        // Write outputs
        out1[i] = sampleL;
        out2[i] = sampleR;
    }
}

float NeveChannelStrip::applySaturation(float sample) {
    // Simple soft-clipping saturation to emulate Neve harmonics
    float drive = saturation * 10.0f; // Saturation intensity
    return (sample > 0) ? std::tanh(drive * sample) : -std::tanh(drive * -sample);
}

float NeveChannelStrip::applyEQ(float sample, float low, float mid, float high) {
    // Simulate frequency-dependent EQ gain adjustments
    float lowGain = low * 1.5f; // Boost low frequencies
    float midGain = mid * 1.2f; // Slight mid-range coloration
    float highGain = high * 1.3f; // High-end shimmer
    return sample * (lowGain + midGain + highGain) / 3.0f;
}

void NeveChannelStrip::setParameter(VstInt32 index, float value) {
    parameters[index] = value;

    switch (index) {
        case GAIN:
            gain = std::pow(10.0f, (value - 0.5f) * 2.0f); // Gain in dB
            break;
        case EQ_LOW:
            eqLow = value;
            break;
        case EQ_MID:
            eqMid = value;
            break;
        case EQ_HIGH:
            eqHigh = value;
            break;
        case SATURATION:
            saturation = value;
            break;
        case COMP_THRESHOLD:
            compThreshold = value * 2.0f - 1.0f; // Threshold between -1 and +1
            break;
        case COMP_RATIO:
            compRatio = 1.0f + value * 19.0f; // Ratio from 1:1 to 20:1
            break;
    }
}

float NeveChannelStrip::getParameter(VstInt32 index) {
    return parameters[index];
}

void NeveChannelStrip::getParameterName(VstInt32 index, char* label) {
    switch (index) {
        case GAIN: std::strcpy(label, "Gain"); break;
        case EQ_LOW: std::strcpy(label, "EQ Low"); break;
        case EQ_MID: std::strcpy(label, "EQ Mid"); break;
        case EQ_HIGH: std::strcpy(label, "EQ High"); break;
        case SATURATION: std::strcpy(label, "Saturation"); break;
        case COMP_THRESHOLD: std::strcpy(label, "Comp Thr"); break;
        case COMP_RATIO: std::strcpy(label, "Comp Ratio"); break;
        default: std::strcpy(label, "Unknown"); break;
    }
}

void NeveChannelStrip::getParameterDisplay(VstInt32 index, char* text) {
    sprintf(text, "%.2f", parameters[index]);
}

void NeveChannelStrip::getParameterLabel(VstInt32 index, char* label) {
    switch (index) {
        case GAIN: std::strcpy(label, "dB"); break;
        case EQ_LOW:
        case EQ_MID:
        case EQ_HIGH: std::strcpy(label, ""); break;
        case SATURATION: std::strcpy(label, ""); break;
        case COMP_THRESHOLD: std::strcpy(label, ""); break;
        case COMP_RATIO: std::strcpy(label, ":1"); break;
        default: std::strcpy(label, ""); break;
    }
}

// Entry point
AudioEffect* createEffectInstance(audioMasterCallback audioMaster) {
    return new NeveChannelStrip(audioMaster);
}


class NeveChannelStripGUI : public NeveChannelStrip {
public:
    NeveChannelStripGUI(audioMasterCallback audioMaster);
    ~NeveChannelStripGUI();

    bool getEffectName(char* name) override;
    bool getProductString(char* text) override;
    bool getVendorString(char* text) override;
    VstInt32 canDo(char* text) override;
    VstPlugCategory getPlugCategory() override;

    // GUI creation
    bool open(void* ptr) override;
    void close() override;

private:
    CFrame* frame;  // Main GUI frame
};

NeveChannelStripGUI::NeveChannelStripGUI(audioMasterCallback audioMaster)
    : NeveChannelStrip(audioMaster), frame(nullptr) {}

NeveChannelStripGUI::~NeveChannelStripGUI() {}

bool NeveChannelStripGUI::getEffectName(char* name) {
    std::strcpy(name, "Neve Channel Strip");
    return true;
}

bool NeveChannelStripGUI::getProductString(char* text) {
    std::strcpy(text, "Neve Channel Strip Plugin");
    return true;
}

bool NeveChannelStripGUI::getVendorString(char* text) {
    std::strcpy(text, "MyPluginCompany");
    return true;
}

VstInt32 NeveChannelStripGUI::canDo(char* text) {
    if (!strcmp(text, "receiveVstEvents")) return 1;
    if (!strcmp(text, "receiveVstMidiEvent")) return 1;
    if (!strcmp(text, "receiveVstTimeInfo")) return 1;
    return -1; // Can't do
}

VstPlugCategory NeveChannelStripGUI::getPlugCategory() {
    return kPlugCategEffect;
}

bool NeveChannelStripGUI::open(void* ptr) {
    AEffEditor* editor = getEditor();
    frame = new CFrame(CRect(0, 0, 400, 300), this);
    frame->open(ptr);

    // Add GUI controls
    CBitmap* background = new CBitmap("background.png");
    frame->setBackground(background);

    // Add controls (e.g., sliders for gain, EQ, etc.)
    CPoint offset(10, 10);
    for (int i = 0; i < NUM_PARAMS; ++i) {
        CVerticalSlider* slider = new CVerticalSlider(
            CRect(offset.x, offset.y, offset.x + 50, offset.y + 200), this, i,
            0.0f, 1.0f, nullptr, nullptr);
        frame->addView(slider);
        offset.x += 60;
    }

    return true;
}

void NeveChannelStripGUI::close() {
    if (frame) {
        frame->close();
        delete frame;
        frame = nullptr;
    }
}

AudioEffect* createEffectInstance(audioMasterCallback audioMaster) {
    return new NeveChannelStripGUI(audioMaster);
}

