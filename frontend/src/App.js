// App.js
import React, { useState } from 'react';
import './App.css'; // Import your CSS file

function App() {
    const [selectedVoice, setSelectedVoice] = useState('Random');
    const [userDescription, setUserDescription] = useState('');
    const [meditationText, setMeditationText] = useState('');

    const handleGenerateMeditation = () => {
        fetch('http://localhost:8000/api/meditation', { // Adjust the URL accordingly
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ voice: selectedVoice, description: userDescription })
        })
        .then(response => response.json())
        .then(data => {
            setMeditationText(data.meditationText);
        })
        .catch(error => console.error('Error:', error));
    };

    return (
        <div className="App">
            <header>
                <h1>AI Guided Meditation</h1>
            </header>
            <main>
                <div className="container">
                    <h2>Find Your Peace</h2>
                    <img src={process.env.PUBLIC_URL + '/monk_meditation4.gif'} alt="Monk" />
                    <div className="input-group">
                        <div className="label-row">
                            <label htmlFor="voice">Voice:</label>
                            <select
                                id="voice"
                                className="voice-dropdown"
                                value={selectedVoice}
                                onChange={(e) => setSelectedVoice(e.target.value)}
                            >
                                <option value="Random">Random</option>
                                <option value="Alloy">Alloy</option>
                                <option value="Echo">Echo</option>
                                <option value="Fable">Fable</option>
                                <option value="Onyx">Onyx</option>
                                <option value="Nova">Nova</option>
                                <option value="Shimmer">Shimmer</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label htmlFor="description">What object would you like as a guru today?</label>
                            <textarea
                                id="description"
                                rows="2"
                                value={userDescription}
                                onChange={(e) => setUserDescription(e.target.value)}
                            ></textarea>
                        </div>
                        <button id="generate-btn" onClick={handleGenerateMeditation}>Generate Meditation</button>
                        <div id="meditation-text">
                            <p>{meditationText}</p>
                        </div>
                    </div>
                </div>
            </main>
            <footer>
                <p>&copy; Armaan Rathi</p>
            </footer>
        </div>
    );
}

export default App;
