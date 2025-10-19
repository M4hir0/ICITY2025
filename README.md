# ICITY2025

Title: BlazeWatch: AI-powered wildfire early alert.

Authors: Daniel Gau, Tiffany Gau

Slides: [Click for Slides](https://docs.google.com/presentation/d/1yoHIYBsCqZywK67ihs82HZD8FoKojqE9bGLHrm9od50/edit?usp=sharing)

## Existing Systems for Wildfire Monitoring

| **System Name**  | **Operating Agency / Key Features**  | **Primary Functions & Monitoring Approach**   |
| ------ | -------- | ------------------ |
| **FIRIS (Fire Integrated Real-Time Intelligence System)** | *California Governor’s Office of Emergency Services (Cal OES)* | Deploys fixed-wing aircraft equipped with advanced infrared and multispectral sensors to collect real-time wildfire data. Information is rapidly transmitted to ground-based systems, providing situational awareness for incident commanders and response teams. ([caloes.ca.gov][1]) |
| **ALERTCalifornia**  | *University of California, San Diego / Public Safety Network*  | Operates a statewide network of over 1,100 high-definition cameras across California’s wildfire-prone regions. The system uses AI-powered image analysis to detect anomalies and issue early alerts to emergency agencies. ([Wikipedia][2])                                            |
| **InciWeb**  | *U.S. Forest Service / Multi-Agency Collaboration* | Serves as a unified national platform for sharing verified information on wildfires and major incidents. Although not a fully real-time monitoring system, it provides official updates, maps, and public safety notices for ongoing events. ([Wikipedia][3])                          |
| **Watch Duty** | *Volunteer-Based Nonprofit Organization* | Combines official data sources with community reports. Supported by trained volunteers, the platform monitors, verifies, and disseminates near real-time wildfire alerts and interactive maps to the public. ([watchduty.org][4])  |

[1]: https://www.caloes.ca.gov/office-of-the-director/operations/response-operations/fire-rescue/firis/?utm_source=chatgpt.com "FIRIS - California Governor's Office of Emergency Services"
[2]: https://en.wikipedia.org/wiki/ALERTCalifornia?utm_source=chatgpt.com "ALERTCalifornia"
[3]: https://en.wikipedia.org/wiki/InciWeb?utm_source=chatgpt.com "InciWeb"
[4]: https://www.watchduty.org/?utm_source=chatgpt.com "Watch Duty - Wildfire Maps & Alerts"

## Common Methods for Wildfire Monitoring

| Method | Advantage | Limitation |
| -------------- | ---------------- | -------------- | ---------- |
| **1. Satellite** | Covers vast areas and can detect heat spots and smoke even in remote regions. | Limited update frequency and resolution; cloud cover can obstruct detection. | 
| **2. Drones** | Provides high-resolution, close-range imagery and can be deployed flexibly.  | Short flight duration, requires operators, and not suitable for continuous monitoring. |
| **3. Surveillance Cameras** | Offers continuous real-time monitoring and can be paired with AI for automatic detection. | Coverage is restricted to installed areas and setup/maintenance costs are high. |
| **4. Phone Reports** | Delivers immediate, ground-truth observations from citizens in real time.  | Reports vary in accuracy and timeliness, and cannot be automatically analyzed. |
| **5. BlazeWatch (AI-Powered Citizen Reporting)** | Uses everyday smartphone photos with AI analysis for instant wildfire detection and alerts. | Depends on user participation and photo quality, and currently limited to populated regions. |



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
