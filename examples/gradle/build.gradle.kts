plugins {
    java
}

group = "com.example"
version = "1.0.0-SNAPSHOT"

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

tasks.jar {
    archiveFileName.set("SentinelExample.jar")
}

// Build with: ./gradlew build
// Upload build/libs/SentinelExample.jar as the dedicated exact-SHA Actions artifact.
