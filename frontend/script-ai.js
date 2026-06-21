let currentIndex = 0;
let answerResults = [];

const questions = [
    "How was your day?",
    "How is your sleep cycle?",
    "Do you feel stress sometimes?",
    "Do you feel crying sometimes for no reason?",
    "Do you want to tell something more?"
];

const questionDivs = [
    document.getElementById("question1"),
    document.getElementById("question2"),
    document.getElementById("question3"),
    document.getElementById("question4"),
    document.getElementById("question5")
];

const inputs = [
    document.getElementById("q1"),
    document.getElementById("q2"),
    document.getElementById("q3"),
    document.getElementById("q4"),
    document.getElementById("q5")
];

const questionTitle = document.getElementById("questionTitle");
const output = document.getElementById("output");
const progressBar = document.querySelector(".progress-bar");
const nextButton = document.querySelector(".analyze-btn");

// INIT
window.onload = function () {
    showQuestion();
};

// SHOW ONLY CURRENT QUESTION
function showQuestion() {

    // hide all questions
    for (let i = 0; i < questionDivs.length; i++) {
        questionDivs[i].style.display = "none";
    }

    // show current
    questionDivs[currentIndex].style.display = "block";

    questionTitle.innerText = `Question ${currentIndex + 1} of 5`;

    progressBar.style.width = ((currentIndex / 5) * 100) + "%";
}

// NEXT BUTTON
function submitAnswer() {

    let answer = inputs[currentIndex].value.trim();

    if (!answer) {
        alert("Please answer before continuing.");
        return;
    }

    nextButton.disabled = true;
    nextButton.innerText = "Saving answer...";

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: questions[currentIndex],
            answer: answer
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        answerResults.push({
            question: questions[currentIndex],
            answer,
            prediction: data.prediction,
            confidence: data.confidence
        });

        currentIndex++;
        progressBar.style.width = `${Math.min((currentIndex / 5) * 100, 100)}%`;

        if (currentIndex < 5) {
            showQuestion();
            nextButton.innerText = "Next Question →";
        } else {
            nextButton.innerText = "Get Final Result";
            getFinalResult();
        }
    })
    .catch(err => {
        console.error(err);
        alert("Unable to submit your answer right now. Please try again.");
        nextButton.innerText = "Next Question →";
    })
    .finally(() => {
        nextButton.disabled = false;
    });
}

// FINAL RESULT
function getFinalResult() {

    progressBar.style.width = "100%";

    fetch("http://127.0.0.1:5000/final", {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        const insight = data.insights || {};
        const summary = insight.summary || "We could not generate a summary at this time.";
        const recommendations = (insight.recommendations || []).map(item => `<li>${item}</li>`).join("");
        const habits = (insight.daily_habits || []).map(item => `<li>${item}</li>`).join("");
        const causes = (insight.possible_causes || []).map(item => `<li>${item}</li>`).join("");
        const displayPrediction = data.display_prediction || data.overall_prediction;

        const resultClass = getResultClass(displayPrediction);

        output.innerHTML = `
            <div class="glass-card result-card ${resultClass}">
                <h2>Your Personalized Mental Wellness Summary</h2>
                <p class="result-tag">Overall Prediction: <strong>${displayPrediction}</strong></p>
                <div class="result-block">
                    <h3>Summary</h3>
                    <p>${summary}</p>
                </div>
                <div class="result-block">
                    <h3>Possible Causes</h3>
                    <ul>${causes}</ul>
                </div>
                <div class="result-block">
                    <h3>Recommendations</h3>
                    <ul>${recommendations}</ul>
                </div>
                <div class="result-block">
                    <h3>Daily Habit Tips</h3>
                    <ul>${habits}</ul>
                </div>
                <p class="disclaimer">${insight.disclaimer || "This is not a medical diagnosis. If you are struggling, consider speaking to a qualified mental health professional."}</p>
            </div>
        `;

        nextButton.style.display = "none";
    })
    .catch(err => {
        console.error(err);
        alert("Unable to generate the final report right now. Please try again.");
        nextButton.disabled = false;
        nextButton.innerText = "Get Final Result";
    });
}

function getResultClass(prediction) {
    const redLabels = ["Depression", "Bipolar", "Suicidal"];
    const yellowLabels = ["Stress", "Anxiety", "Personality disorder"];

    if (prediction === "Normal") {
        return "result-green";
    }
    if (yellowLabels.includes(prediction)) {
        return "result-yellow";
    }
    if (redLabels.includes(prediction)) {
        return "result-red";
    }
    return "result-yellow";
}