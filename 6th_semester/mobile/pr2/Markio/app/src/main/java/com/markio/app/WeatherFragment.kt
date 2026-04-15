package com.markio.app

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment

class WeatherFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_weather, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Static data is already set in XML
        // Additional static data can be set here if needed
        val tvCityName = view.findViewById<TextView>(R.id.tvCityName)
        val tvWeatherDate = view.findViewById<TextView>(R.id.tvWeatherDate)
        val tvTemperature = view.findViewById<TextView>(R.id.tvTemperature)

        tvCityName.text = "Тестоград"
        tvWeatherDate.text = "Вс, 22 февраля"
        tvTemperature.text = "-1°"
    }
}
