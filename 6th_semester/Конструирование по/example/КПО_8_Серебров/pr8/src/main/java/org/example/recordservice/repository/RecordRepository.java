package org.example.recordservice.repository;

import org.example.recordservice.model.JobRecord;
import org.example.recordservice.model.IResume;
import org.example.recordservice.model.IVacancy;

import java.sql.*;

/**
 * RecordRepository — репозиторий данных RecordService.
 * Каждый микросервис имеет собственную изолированную схему БД
 * (принцип Database per Service в микросервисной архитектуре).
 */
public class RecordRepository {
    private Connection connection;

    public RecordRepository(Connection connection) {
        this.connection = connection;
    }

    public void insertRecord(JobRecord record) {
        try {
            String sql = "INSERT INTO records (id, owner_id, type, data) VALUES (?, ?, ?, ?)";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, record.getId());
            stmt.setString(2, record.getId());
            stmt.setString(3, record.getClass().getSimpleName());
            stmt.setObject(4, record.getNonSpecificData());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void updateRecord(JobRecord record) {
        try {
            String sql = "UPDATE records SET data = ?, is_promoted = true WHERE id = ?";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setObject(1, record.getNonSpecificData());
            stmt.setString(2, record.getId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void deleteRecord(String recordId) {
        try {
            String sql = "DELETE FROM records WHERE id = ?";
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, recordId);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
