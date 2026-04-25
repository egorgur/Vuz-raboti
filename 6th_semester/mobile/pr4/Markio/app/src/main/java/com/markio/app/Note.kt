package com.markio.app

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Data class representing a note in the Markio app.
 */
@Entity(tableName = "notes")
data class Note(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    var title: String,
    var text: String,
    val date: String
)
