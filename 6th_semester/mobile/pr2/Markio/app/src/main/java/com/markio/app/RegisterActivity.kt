package com.markio.app

import android.content.Intent
import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton

class RegisterActivity : AppCompatActivity() {

    private lateinit var etEmail: EditText
    private lateinit var etPassword: EditText
    private lateinit var btnCreateAccount: MaterialButton
    private lateinit var tvLoginLink: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        etEmail = findViewById(R.id.etRegEmail)
        etPassword = findViewById(R.id.etRegPassword)
        btnCreateAccount = findViewById(R.id.btnCreateAccount)
        tvLoginLink = findViewById(R.id.tvLoginLink)

        btnCreateAccount.setOnClickListener {
            val email = etEmail.text.toString().trim()
            val password = etPassword.text.toString().trim()

            if (email.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Заполните все поля", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            Toast.makeText(this, "Аккаунт создан!", Toast.LENGTH_SHORT).show()

            // Navigate to main screen
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
            finish()
        }

        tvLoginLink.setOnClickListener {
            finish() // Go back to login
        }
    }
}
