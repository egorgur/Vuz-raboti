package org.example.recordservice.model;

public class VacancyImpl extends JobRecord implements IVacancy {
    Object vacancySpecificData;

    @Override
    public void setVacancySpecificData(Object vacancySpecificData) {
        this.vacancySpecificData = vacancySpecificData;
    }

    @Override
    public Object getVacancySpecificData() {
        return vacancySpecificData;
    }
}
