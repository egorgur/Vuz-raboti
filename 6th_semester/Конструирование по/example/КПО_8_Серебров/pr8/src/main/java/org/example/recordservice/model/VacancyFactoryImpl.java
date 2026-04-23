package org.example.recordservice.model;

public class VacancyFactoryImpl extends RecordFactory {

    @Override
    public JobRecord getRecordWithNonSpecificData(Object nonSpecificData) {
        VacancyImpl vacancy = new VacancyImpl();
        vacancy.setNonSpecificData(nonSpecificData);
        return vacancy;
    }

    @Override
    public JobRecord getRecordWithSpecificData(JobRecord record, Object vacancySpecificData) {
        VacancyImpl vacancy = (VacancyImpl) record;
        vacancy.setVacancySpecificData(vacancySpecificData);
        return vacancy;
    }
}
