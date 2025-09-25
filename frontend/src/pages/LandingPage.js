// src/pages/LandingPage.js
import React from 'react';
import Hero from '../components/Landing/Hero';
import TrustSection from '../components/Landing/TrustSection';
import UsageGuide from '../components/Landing/UsageGuide';
import Features from '../components/Landing/Features';
import Value from '../components/Landing/Value';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <Hero />
      <TrustSection />
      <UsageGuide />
      <Features />
      <Value />
    </div>
  );
};

export default LandingPage;