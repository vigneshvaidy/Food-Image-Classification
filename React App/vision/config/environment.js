var environments = {
  staging: {
    FIREBASE_API_KEY: 'AIzaSyDPdO5MKSHnmArLC3kGXjHL_VG0vf-DNUM',
    FIREBASE_AUTH_DOMAIN: 'foodscanner.firebaseapp.com',
    FIREBASE_DATABASE_URL: 'https://foodscanner.firebaseio.com',
    FIREBASE_PROJECT_ID: 'foodscanner',
    FIREBASE_STORAGE_BUCKET: 'foodscanner.appspot.com',
    FIREBASE_MESSAGING_SENDER_ID: '912194317489',
    GOOGLE_CLOUD_VISION_API_KEY: 'AIzaSyB5GDkh98odeEdJs4UC8BaYgr01zs-gpi0'
  },
  production: {
  }
};

function getReleaseChannel() {
  let releaseChannel = Expo.Constants.manifest.releaseChannel;
  if (releaseChannel === undefined) {
    return 'staging';
  } else if (releaseChannel === 'staging') {
    return 'staging';
  } else {
    return 'staging';
  }
}
function getEnvironment(env) {
  console.log('Release Channel: ', getReleaseChannel());
  return environments[env];
}
var Environment = getEnvironment(getReleaseChannel());
export default Environment;