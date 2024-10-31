// FILE: djangify_frontend/pages/about.tsx
import React from 'react';
import Layout from '../components/Layout'; // Adjust the path as necessary

const About = () => {
  return (
    <Layout>
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">About Us</h1>
        <p className="text-lg">
          Welcome to our website. We are dedicated to providing the best service.
        </p>
      </div>
    </Layout>
  );
};

export default About;
