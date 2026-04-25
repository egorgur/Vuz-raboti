package com.markio.app

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class NotesAdapter(
    private val notes: MutableList<Note>,
    private val onEditClick: (Note) -> Unit,
    private val onDeleteClick: (Note) -> Unit
) : RecyclerView.Adapter<NotesAdapter.NoteViewHolder>() {

    class NoteViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvTitle: TextView = itemView.findViewById(R.id.tvNoteTitle)
        val tvText: TextView = itemView.findViewById(R.id.tvNoteText)
        val tvDate: TextView = itemView.findViewById(R.id.tvNoteDate)
        val btnEdit: ImageView = itemView.findViewById(R.id.btnEditNote)
        val btnDelete: ImageView = itemView.findViewById(R.id.btnDeleteNote)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NoteViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_note, parent, false)
        return NoteViewHolder(view)
    }

    override fun onBindViewHolder(holder: NoteViewHolder, position: Int) {
        val note = notes[position]
        holder.tvTitle.text = note.title
        holder.tvText.text = note.text
        holder.tvDate.text = note.date

        holder.btnEdit.setOnClickListener {
            onEditClick(note)
        }

        holder.btnDelete.setOnClickListener {
            onDeleteClick(note)
        }
    }

    override fun getItemCount(): Int = notes.size

    fun setNotes(newNotes: List<Note>) {
        notes.clear()
        notes.addAll(newNotes)
        notifyDataSetChanged()
    }

    fun removeNote(note: Note) {
        val position = notes.indexOf(note)
        if (position != -1) {
            notes.removeAt(position)
            notifyItemRemoved(position)
        }
    }

    fun addNote(note: Note) {
        notes.add(0, note)
        notifyItemInserted(0)
    }

    fun updateNote(note: Note) {
        val position = notes.indexOfFirst { it.id == note.id }
        if (position != -1) {
            notes[position] = note
            notifyItemChanged(position)
        }
    }
}
