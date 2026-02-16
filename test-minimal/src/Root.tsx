import {Composition} from 'remotion';
import {HelloWorld} from './HelloWorld';
import {AnimatedText} from './AnimatedText';
import {CustomText} from './CustomText';
import {SimpleTest} from './SimpleTest';
import {AnimatedWords} from './AnimatedWords';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SimpleTest"
        component={SimpleTest}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="AnimatedWords"
        component={AnimatedWords}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="AnimatedText"
        component={AnimatedText}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="CustomText"
        component={CustomText}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'TEXTO ANIMADO',
          subtitle: 'Renderizado con Remotion + FastAPI',
          words: ['VIDEO', 'PERSONALIZADO', 'DESDE', 'N8N', '💪']
        }}
      />
    </>
  );
};
