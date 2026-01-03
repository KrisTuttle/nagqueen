<template>
  <div class="landing">
    <section class="hero">
      <h1>Nag Queen</h1>
      <p class="tagline">Your personal reminder service that actually texts you</p>
      <router-link to="/login" class="cta-btn">Get Started</router-link>
    </section>

    <section class="features">
      <div class="feature">
        <div class="feature-icon">&#128242;</div>
        <h3>SMS Reminders</h3>
        <p>Get text messages for the things that matter. No app to check, no notifications to miss.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">&#128337;</div>
        <h3>Flexible Scheduling</h3>
        <p>One-time, daily, weekly, or monthly. Set it and forget it.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">&#128274;</div>
        <h3>No Email Required</h3>
        <p>Sign in with just your phone number. Simple and private.</p>
      </div>
    </section>

    <section class="how-it-works">
      <h2>How it works</h2>
      <div class="steps">
        <div class="step">
          <span class="step-num">1</span>
          <p>Sign up with your phone number</p>
        </div>
        <div class="step">
          <span class="step-num">2</span>
          <p>Create your reminders</p>
        </div>
        <div class="step">
          <span class="step-num">3</span>
          <p>Get texts when you need them</p>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <h2>Never forget again</h2>
      <router-link to="/login" class="cta-btn">Start Now</router-link>
    </section>

    <footer>
      <p>Nag Queen</p>
    </footer>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero {
  text-align: center;
  padding: 6rem 2rem 4rem;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.tagline {
  font-size: 1.4rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.cta-btn {
  display: inline-block;
  background: white;
  color: #6366f1;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.feature {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.feature p {
  opacity: 0.85;
  line-height: 1.5;
}

.how-it-works {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(0, 0, 0, 0.1);
}

.how-it-works h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.steps {
  display: flex;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.step-num {
  width: 50px;
  height: 50px;
  background: white;
  color: #6366f1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
}

.step p {
  font-size: 1.1rem;
  max-width: 200px;
}

.cta-section {
  text-align: center;
  padding: 4rem 2rem;
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

footer {
  text-align: center;
  padding: 2rem;
  opacity: 0.7;
  font-size: 0.9rem;
}
</style>
