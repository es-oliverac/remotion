import { getCompositions } from '@remotion/renderer';

async function test() {
  try {
    console.log('Testing with studio server...');
    const comps = await getCompositions('http://localhost:3000');
    console.log('✅ SUCCESS! Compositions:', comps.length);
    console.log('Composition:', comps[0]?.id);
  } catch (error) {
    console.log('❌ FAILED:', error.message);
  }
}

test();
