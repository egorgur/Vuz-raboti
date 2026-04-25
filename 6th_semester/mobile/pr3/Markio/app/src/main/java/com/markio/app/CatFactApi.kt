package com.markio.app

import retrofit2.http.GET

data class CatFact(
    val fact: String,
    val length: Int
)

interface CatFactApi {
    @GET("fact")
    suspend fun getFact(): CatFact
}
