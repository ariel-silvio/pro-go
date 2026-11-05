export const CONFIG = {
  FEEDBACK_FORM_URL: 'TODO_ARIEL_GOOGLE_FORM_URL', // append ?variant= and &persona=
  AED_PER_EUR: 4.2,
  PILOT_CITY: 'Dubai',
  PILOT_COMMUNITIES: ['Downtown Dubai', 'Business Bay'], // D14 proposed, confirm
  SALON_SHARE_DEFAULT: 0.35,
  STORAGE_KEY: 'progo-demo-v1',
};

export const feedbackReady = () => CONFIG.FEEDBACK_FORM_URL.startsWith('https://');
