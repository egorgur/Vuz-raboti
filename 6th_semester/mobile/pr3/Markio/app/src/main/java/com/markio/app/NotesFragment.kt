package com.markio.app

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton

class NotesFragment : Fragment() {

    private lateinit var rvNotes: RecyclerView
    private lateinit var btnCreateNote: MaterialButton
    private lateinit var noteFormContainer: LinearLayout
    private lateinit var etNoteTitle: EditText
    private lateinit var etNoteText: EditText
    private lateinit var btnSaveNote: MaterialButton
    private lateinit var btnCancelNote: MaterialButton

    private lateinit var adapter: NotesAdapter
    private val notesList = mutableListOf<Note>()
    private var editingNote: Note? = null
    private var nextId = 1

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_notes, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        rvNotes = view.findViewById(R.id.rvNotes)
        btnCreateNote = view.findViewById(R.id.btnCreateNote)
        noteFormContainer = view.findViewById(R.id.noteFormContainer)
        etNoteTitle = view.findViewById(R.id.etNoteTitle)
        etNoteText = view.findViewById(R.id.etNoteText)
        btnSaveNote = view.findViewById(R.id.btnSaveNote)
        btnCancelNote = view.findViewById(R.id.btnCancelNote)

        // Add static sample notes
        addSampleNotes()

        // Setup RecyclerView
        adapter = NotesAdapter(
            notesList,
            onEditClick = { note -> startEditNote(note) },
            onDeleteClick = { note -> deleteNote(note) }
        )
        rvNotes.layoutManager = LinearLayoutManager(requireContext())
        rvNotes.adapter = adapter

        // Create note button
        btnCreateNote.setOnClickListener {
            editingNote = null
            etNoteTitle.setText("")
            etNoteText.setText("")
            noteFormContainer.visibility = View.VISIBLE
        }

        // Save note
        btnSaveNote.setOnClickListener {
            val title = etNoteTitle.text.toString().trim()
            val text = etNoteText.text.toString().trim()

            if (title.isEmpty()) {
                Toast.makeText(requireContext(), "Введите заголовок", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            if (editingNote != null) {
                // Update existing note
                editingNote!!.title = title
                editingNote!!.text = text
                adapter.updateNote(editingNote!!)
            } else {
                // Create new note
                val note = Note(
                    id = nextId++,
                    title = title,
                    text = text,
                    date = "22 февраля 2026"
                )
                adapter.addNote(note)
            }

            noteFormContainer.visibility = View.GONE
            editingNote = null
        }

        // Cancel
        btnCancelNote.setOnClickListener {
            noteFormContainer.visibility = View.GONE
            editingNote = null
        }
    }

    private fun addSampleNotes() {
        notesList.add(
            Note(
                id = nextId++,
                title = "Заголовок",
                text = "Тест",
                date = "22 февраля 2026"
            )
        )
        notesList.add(
            Note(
                id = nextId++,
                title = "Покупки",
                text = "Молоко, хлеб, яйца",
                date = "22 февраля 2026"
            )
        )
        notesList.add(
            Note(
                id = nextId++,
                title = "Идеи для проекта",
                text = "Мобильное приложение для заметок",
                date = "21 февраля 2026"
            )
        )
    }

    private fun startEditNote(note: Note) {
        editingNote = note
        etNoteTitle.setText(note.title)
        etNoteText.setText(note.text)
        noteFormContainer.visibility = View.VISIBLE
    }

    private fun deleteNote(note: Note) {
        adapter.removeNote(note)
    }
}
