package com.markio.app

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

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
    
    private val database by lazy { AppDatabase.getDatabase(requireContext()) }
    private val noteDao by lazy { database.noteDao() }

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

        // Setup RecyclerView
        adapter = NotesAdapter(
            notesList,
            onEditClick = { note -> startEditNote(note) },
            onDeleteClick = { note -> deleteNote(note) }
        )
        rvNotes.layoutManager = LinearLayoutManager(requireContext())
        rvNotes.adapter = adapter

        // Observe notes from DB
        lifecycleScope.launch {
            noteDao.getAllNotes().collect { notes ->
                adapter.setNotes(notes)
            }
        }

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

            val currentDate = SimpleDateFormat("dd MMMM yyyy", Locale("ru")).format(Date())

            lifecycleScope.launch {
                if (editingNote != null) {
                    // Update existing note
                    val updatedNote = editingNote!!.copy(title = title, text = text)
                    noteDao.updateNote(updatedNote)
                } else {
                    // Create new note
                    val note = Note(
                        title = title,
                        text = text,
                        date = currentDate
                    )
                    noteDao.insertNote(note)
                }
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

    private fun startEditNote(note: Note) {
        editingNote = note
        etNoteTitle.setText(note.title)
        etNoteText.setText(note.text)
        noteFormContainer.visibility = View.VISIBLE
    }

    private fun deleteNote(note: Note) {
        lifecycleScope.launch {
            noteDao.deleteNote(note)
        }
    }
}
