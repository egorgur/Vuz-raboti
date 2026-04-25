package com.markio.app

import android.os.Bundle
import android.preference.PreferenceManager
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class WeatherFragment : Fragment() {

    private lateinit var mapView: MapView
    private lateinit var tvCatFact: TextView

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Initialize osmdroid configuration
        Configuration.getInstance().load(requireContext(), PreferenceManager.getDefaultSharedPreferences(requireContext()))
        return inflater.inflate(R.layout.fragment_weather, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        tvCatFact = view.findViewById(R.id.tvCatFact)
        mapView = view.findViewById(R.id.map)

        setupMap()
        fetchCatFact()
    }

    private fun setupMap() {
        mapView.setTileSource(TileSourceFactory.MAPNIK)
        mapView.setMultiTouchControls(true)

        val mapController = mapView.controller
        mapController.setZoom(12.0)
        
        // Default point (e.g., Moscow)
        val startPoint = GeoPoint(55.7558, 37.6173)
        mapController.setCenter(startPoint)

        // Add a marker
        val marker = Marker(mapView)
        marker.position = startPoint
        marker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM)
        marker.title = "Москва"
        marker.snippet = "Столица России"
        mapView.overlays.add(marker)

        // Add another marker
        val marker2 = Marker(mapView)
        marker2.position = GeoPoint(55.7512, 37.6297)
        marker2.title = "Парк Зарядье"
        marker2.snippet = "Красивый современный парк"
        mapView.overlays.add(marker2)
    }

    private fun fetchCatFact() {
        val retrofit = Retrofit.Builder()
            .baseUrl("https://catfact.ninja/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val api = retrofit.create(CatFactApi::class.java)

        lifecycleScope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    api.getFact()
                }
                tvCatFact.text = response.fact
            } catch (e: Exception) {
                tvCatFact.text = "Ошибка загрузки факта: ${e.message}"
            }
        }
    }

    override fun onResume() {
        super.onResume()
        mapView.onResume()
    }

    override fun onPause() {
        super.onPause()
        mapView.onPause()
    }
}
