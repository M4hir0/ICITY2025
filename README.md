# ICITY2025

Title: BlazeWatch: AI-powered wildfire early alert.

Authors: Daniel Gau, Tiffany Gau

Slides: [Click for Slides](https://docs.google.com/presentation/d/1yoHIYBsCqZywK67ihs82HZD8FoKojqE9bGLHrm9od50/edit?usp=sharing)

## Technology Used

**Web Framework**

* [Flask Documentation](https://flask.palletsprojects.com/en/stable/)

**LLM**

* [Google Gemini API](https://aistudio.google.com/)

**Image Hosting**

* [imgbb](https://imgbb.com/)
* [SM.MS](https://sm.ms/) (Considering)

**Voice Hosting**

* [vocaroo](https://vocaroo.com/) (To use in Eco-Tourism!)

**Database**

* [firebase](https://firebase.google.com/)
* [supabase](https://supabase.com/) (Considering trying this open source firebase alternative)

**WebGIS**

* [leaflet.js](https://leafletjs.com/)

**Real-time Notification**

* [Telegram Messenger](https://telegram.org/)

**Deployment**

* [Render](https://render.com/)

## Demo Websites

* [BlazeWatch](https://icity2025.onrender.com/)
* [Task List](https://m4hir0.github.io/ICITY2025)
* [Task Control Panel](https://m4hir0.github.io/ICITY2025/update.html)

Note that, for security purposes, the firestore access would have been set to readonly.

```
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read: if true;     // allow read
      allow write: if false;   // not allow write
    }
  }
}
```
