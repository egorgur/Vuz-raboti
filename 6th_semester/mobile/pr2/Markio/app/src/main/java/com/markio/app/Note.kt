package com.markio.app

/**
 * Data class representing a note in the Markio app.
 */
data class Note(
    val id: Int,
    var title: String,
    var text: String,
    val date: String
)
