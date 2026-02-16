import {AbsoluteFill} from 'remotion';

export const SimpleTest: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'red',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: 120,
          fontWeight: 900,
          color: 'white',
          textAlign: 'center',
          fontFamily: 'Arial, Helvetica, sans-serif',
          textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
          WebkitTextStroke: '2px black',
        }}
      >
        SI VEO ESTO, FUNCIONA
      </div>
    </AbsoluteFill>
  );
};
