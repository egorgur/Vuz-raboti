package com.markio.app

import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment

class MainActivity : AppCompatActivity() {

    private lateinit var tabWeather: TextView
    private lateinit var tabNotes: TextView
    private lateinit var btnLogout: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tabWeather = findViewById(R.id.tabWeather)
        tabNotes = findViewById(R.id.tabNotes)
        btnLogout = findViewById(R.id.btnLogout)

        // Show weather fragment by default
        if (savedInstanceState == null) {
            showFragment(WeatherFragment())
            updateTabs(isWeatherActive = true)
        }

        tabWeather.setOnClickListener {
            showFragment(WeatherFragment())
            updateTabs(isWeatherActive = true)
        }

        tabNotes.setOnClickListener {
            showFragment(NotesFragment())
            updateTabs(isWeatherActive = false)
        }

        btnLogout.setOnClickListener {
            val intent = Intent(this, LoginActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
            finish()
        }
    }

    private fun showFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.contentContainer, fragment)
            .commit()
    }

    private fun updateTabs(isWeatherActive: Boolean) {
        if (isWeatherActive) {
            tabWeather.setBackgroundResource(R.drawable.bg_tab_active)
            tabNotes.setBackgroundResource(R.drawable.bg_tab_inactive)
        } else {
            tabWeather.setBackgroundResource(R.drawable.bg_tab_inactive)
            tabNotes.setBackgroundResource(R.drawable.bg_tab_active)
        }
    }
}
