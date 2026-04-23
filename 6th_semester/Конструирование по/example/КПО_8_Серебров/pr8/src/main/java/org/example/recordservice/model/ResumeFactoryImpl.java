package org.example.recordservice.model;

public class ResumeFactoryImpl extends RecordFactory {

    @Override
    public JobRecord getRecordWithNonSpecificData(Object nonSpecificData) {
        ResumeImpl resume = new ResumeImpl();
        resume.setNonSpecificData(nonSpecificData);
        return resume;
    }

    @Override
    public JobRecord getRecordWithSpecificData(JobRecord record, Object resumeSpecificData) {
        ResumeImpl resume = (ResumeImpl) record;
        resume.setResumeSpecificData(resumeSpecificData);
        return resume;
    }
}
