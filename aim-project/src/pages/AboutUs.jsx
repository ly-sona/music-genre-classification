// src/pages/AboutUs.jsx
import React from 'react';
import AnuImage from '../assets/AIMProjectAnu.png'
import AgnusImage from '../assets/AIMProjectAgnus.png'
import RishiImage from '../assets/AIMProjectRishi.png'
import OwenImage from '../assets/AIMProjectOwen.png'
import YashImage from '../assets/AIMProjectYash.png'

function AboutUs() {
  const teamMembers = [
    {
      name: 'Anu Boyapati',
      image: AnuImage,
      description: 'Junior in Computer Science and hobbyist writer.',
      linkedin: 'https://linkedin.com/in/anushrutha-boyapati',
      github: 'https://github.com/ly-sona',
    },
    {
      name: 'Agnus Thomas',
      image: AgnusImage,
      description: 'Junior in Computer Science and loves games.',
      linkedin: 'https://www.linkedin.com/in/agnus-thom/',
      github: 'https://github.com/raspberryhelp',
    },
    {
      name: 'Owen Walters',
      image: OwenImage,
      description: 'Sophomore in Computer Science with a love for math.',
      linkedin: 'https://www.linkedin.com/in/owen-walters-233980215',
      github: 'https://github.com/OWalters-Hub',
    },
    {
      name: 'Rishi Chodavarapu',
      image: RishiImage, 
      description: 'Junior in Computer Science and loves movies.',
      linkedin: 'https://www.linkedin.com/in/rishinaiducs/',
      github: 'hhttps://github.com/Rishi-Naidu',
    },
    {
      name: 'Yash Baruah',
      image: YashImage,
      description: 'Freshman in Computer Science and likes to read.',
      linkedin: 'https://www.linkedin.com/in/yashbaruah/',
      github: 'https://github.com/bornayo7',
    },
    {
      name: 'Skye Drechsler',
      image: 'AIMProjectAnu.png', // Replace with actual path or import
      description: 'Sophomore in Computer Science and likes baseball.',
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
              className="flex flex-col items-center bg-slate-200 rounded-lg shadow-lg p-6"
            >
              <div className="w-32 h-32 mb-4">
                <img
                  src={member.image}
                  alt={member.name}
                  className="object-cover w-full h-full rounded-lg"
                />
              </div>
              <h3 className="text-xl font-semibold text-purple-700 mb-2">
                {member.name}
              </h3>
              <p className="text-center text-purple-600 mb-4">
                {member.description}
              </p>
              <div className="flex space-x-4">
              <a
                href={member.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="text-white bg-[#007ebb] hover:bg-[#007ebb]/90 focus:ring-4 focus:outline-none focus:ring-[#007ebb]/50 font-medium rounded-lg text-sm px-5 py-2.5 inline-flex items-center mb-2"
              >
                {/* LinkedIn SVG Icon */}
                <svg
                  className="w-4 h-4 mr-2"
                  fill="currentColor"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 260.366 260.366"
                  aria-hidden="true"
                >
                  <g>
                    <path d="M34.703,0.183C15.582,0.183,0.014,15.748,0,34.884C0,54.02,15.568,69.588,34.703,69.588c19.128,0,34.688-15.568,34.688-34.704C69.391,15.75,53.83,0.183,34.703,0.183z" />
                    <path d="M60.748,83.531H8.654c-2.478,0-4.488,2.009-4.488,4.489v167.675c0,2.479,2.01,4.488,4.488,4.488h52.093c2.479,0,4.489-2.01,4.489-4.488V88.02C65.237,85.539,63.227,83.531,60.748,83.531z" />
                    <path d="M193.924,81.557c-19.064,0-35.817,5.805-46.04,15.271V88.02c0-2.48-2.01-4.489-4.489-4.489H93.424c-2.479,0-4.489,2.009-4.489,4.489v167.675c0,2.479,2.01,4.488,4.489,4.488h52.044c2.479,0,4.489-2.01,4.489-4.488v-82.957c0-23.802,4.378-38.555,26.227-38.555c21.526,0.026,23.137,15.846,23.137,39.977v81.535c0,2.479,2.01,4.488,4.49,4.488h52.068c2.478,0,4.488-2.01,4.488-4.488v-91.977C260.366,125.465,252.814,81.557,193.924,81.557z" />
                  </g>
                </svg>
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