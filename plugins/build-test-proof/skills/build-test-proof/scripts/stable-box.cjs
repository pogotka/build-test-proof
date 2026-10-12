// Optional browser-independent helper: adapt getBox to the supported host API.
const {performance} = require('node:perf_hooks');
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function waitForStableBox(getBox, options = {}) {
  const {timeoutMs=4000,stableMs=300,intervalMs=100,tolerance=0.5} = options;
  if(typeof getBox !== 'function' || ![timeoutMs,stableMs,intervalMs,tolerance].every(Number.isFinite) || timeoutMs<=0 || stableMs<0 || intervalMs<=0 || tolerance<0 || stableMs>=timeoutMs) throw new Error('Invalid stable-box callback/options');
  const start=performance.now();let anchor=null,stableSince=null;
  while(performance.now()-start < timeoutMs) {
    let timer,box;
    const remaining=timeoutMs-(performance.now()-start);
    try {
      box=await Promise.race([Promise.resolve().then(getBox), new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error(`Geometry read exceeded ${timeoutMs}ms budget`)),remaining);})]);
    } finally {clearTimeout(timer);}
    const now=performance.now();
    const valid=box && ['x','y','width','height'].every(k=>Number.isFinite(box[k])) && box.width>0 && box.height>0;
    if(!valid){anchor=null;stableSince=null;}
    else {
      const changed=!anchor || ['x','y','width','height'].some(k=>Math.abs(box[k]-anchor[k])>tolerance);
      if(changed){anchor={x:box.x,y:box.y,width:box.width,height:box.height};stableSince=now;}
      // Compare against the anchor, not the previous sample: slow drift is movement.
      else if(now-stableSince>=stableMs && now-start<timeoutMs) return {...box};
    }
    await delay(Math.min(intervalMs,Math.max(0,timeoutMs-(performance.now()-start))));
  }
  throw new Error(`Element geometry did not stabilize within ${timeoutMs}ms. Refresh state and diagnose; do not drag using old coordinates.`);
}
module.exports={waitForStableBox};
