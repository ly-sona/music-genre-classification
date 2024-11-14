// src/pages/AboutUs.jsx
import React from 'react';

function AboutUs() {
  const teamMembers = [
    {
      name: 'Anu Boyapati',
      image: 'AIMProjectAnu.png', // Use the imported image
      description: 'Junior in Computer Science and hobbyist writer.',
      linkedin: 'https://linkedin.com/in/anushrutha-boyapati',
      github: 'https://github.com/ly-sona',
    },
    {
      name: 'Bob Smith',
      image: 'AIMProjectAnu.png', // Replace with actual path or import
      description: 'Machine Learning Engineer specializing in audio analysis.',
      linkedin: 'https://linkedin.com/in/bobsmith',
      github: 'https://github.com/bobsmith',
    },
    {
      name: 'Carol Williams',
      image: 'AIMProjectAnu.png', // Replace with actual path or import
      description: 'UI/UX Designer with a love for creating intuitive interfaces.',
      linkedin: 'https://linkedin.com/in/carolwilliams',
      github: 'https://github.com/carolwilliams',
    },
    {
      name: 'David Brown',
      image: 'AIMProjectAnu.png', // Replace with actual path or import
      description: 'Backend Developer focused on scalable systems.',
      linkedin: 'https://linkedin.com/in/davidbrown',
      github: 'https://github.com/davidbrown',
    },
    {
      name: 'Eve Davis',
      image: 'AIMProjectAnu.png', // Replace with actual path or import
      description: 'Data Scientist with a knack for finding patterns in data.',
      linkedin: 'https://linkedin.com/in/evedavis',
      github: 'https://github.com/evedavis',
    },
    {
      name: 'Eve Davis',
      image: 'AIMProjectAnu.png', // Replace with actual path or import
      description: 'Data Scientist with a knack for finding patterns in data.',
      linkedin: 'https://linkedin.com/in/evedavis',
      github: 'https://github.com/evedavis',
    },
  ];

  return (
    <div className="relative py-24 flex justify-center">
      <section className="relative w-full max-w-6xl p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl z-20 border border-white/10 overflow-hidden">
        {/* Background Radial Gradient */}
        <div
          className="absolute top-0 left-0 z-[-2] h-full w-full bg-white 
            bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%, 
            rgba(120,119,198,0.3), rgba(255,255,255,0))]"
        ></div>

        {/* Heading */}
        <h2 className="text-3xl md:text-5xl font-extrabold text-purple-600 mb-8 drop-shadow-md text-center">
          Meet the Team
        </h2>

        {/* Team Members Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {teamMembers.map((member, index) => (
            <div
              key={index}
              className="flex flex-col items-center bg-slate-900 rounded-lg shadow-lg p-6"
            >
              <div className="w-32 h-32 mb-4">
                <img
                  src={member.image}
                  alt={member.name}
                  className="object-cover w-full h-full rounded-lg"
                />
              </div>
              <h3 className="text-xl font-semibold text-purple-600 mb-2">
                {member.name}
              </h3>
              <p className="text-center text-purple-500 mb-4">
                {member.description}
              </p>
              <div className="flex space-x-4">
                <a
                  href={member.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-700 text-white rounded-lg shadow-lg hover:from-blue-600 hover:to-blue-800 transition duration-300"
                >
                  LinkedIn
                </a>
                {/* Updated GitHub Button */}
                <a
                  href={member.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-white bg-[#24292F] hover:bg-[#24292F]/90 focus:ring-4 focus:outline-none focus:ring-[#24292F]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500 dark:hover:bg-[#050708]/30 me-2 mb-2"
                >
                  {/* GitHub SVG Icon */}
                  <svg
                    className="w-4 h-4 mr-2" // Changed 'me-2' to 'mr-2' for margin-right
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 .333A9.911 9.911 0 0 0 6.866 19.65c.5.092.678-.215.678-.477 0-.237-.01-1.017-.014-1.845-2.757.6-3.338-1.169-3.338-1.169a2.627 2.627 0 0 0-1.1-1.451c-.9-.615.07-.6.07-.6a2.084 2.084 0 0 1 1.518 1.021 2.11 2.11 0 0 0 2.884.823c.044-.503.268-.973.63-1.325-2.2-.25-4.516-1.1-4.516-4.9A3.832 3.832 0 0 1 4.7 7.068a3.56 3.56 0 0 1 .095-2.623s.832-.266 2.726 1.016a9.409 9.409 0 0 1 4.962 0c1.89-1.282 2.717-1.016 2.717-1.016.366.83.402 1.768.1 2.623a3.827 3.827 0 0 1 1.02 2.659c0 3.807-2.319 4.644-4.525 4.889a2.366 2.366 0 0 1 .673 1.834c0 1.326-.012 2.394-.012 2.72 0 .263.18.572.681.475A9.911 9.911 0 0 0 10 .333Z"
                      clipRule="evenodd"
                    />
                  </svg>
                  GitHub
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default AboutUs;