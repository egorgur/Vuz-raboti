package org.example.recordservice.model;

public class ResumeImpl extends JobRecord implements IResume {
    Object resumeSpecificData;

    @Override
    public void setResumeSpecificData(Object resumeSpecificData) {
        this.resumeSpecificData = resumeSpecificData;
    }

    @Override
    public Object getResumeSpecificData() {
        return resumeSpecificData;
    }
}
