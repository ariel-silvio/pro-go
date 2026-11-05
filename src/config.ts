export const CONFIG = {
  // Google Form link. Use the form's "Get pre-filled link" and paste the part before the first "entry.".
  // Example: 'https://docs.google.com/forms/d/e/XXXX/viewform'
  FEEDBACK_FORM_URL: 'TODO_ARIEL_GOOGLE_FORM_URL',
  // Google Forms prefill uses entry IDs, not names. Replace with e.g. 'entry.123456789'.
  FEEDBACK_FIELDS: { variant: 'variant', persona: 'persona', plan: 'plan' } as Record<string, string>,
  AED_PER_EUR: 4.2,
  SHOW_EUR: true, // open item: AED only, or AED plus euro
  PILOT_CITY: 'Dubai',
  PILOT_COMMUNITIES: ['Downtown Dubai', 'Business Bay'], // D14 proposed, confirm
  SALON_SHARE_DEFAULT: 0.35,
  STORAGE_KEY: 'progo-demo-v1',
};

export const feedbackReady = () => CONFIG.FEEDBACK_FORM_URL.startsWith('https://');

export function feedbackUrl(params: Record<string, string> = {}) {
  const url = new URL(CONFIG.FEEDBACK_FORM_URL);
  url.searchParams.set('usp', 'pp_url');
  Object.entries(params).forEach(([k, v]) => url.searchParams.set(CONFIG.FEEDBACK_FIELDS[k] ?? k, v));
  return url.toString();
}

export const aed = (n: number) => `AED ${n.toLocaleString('en-GB')}`;
export const eur = (n: number) => `€${Math.round(n / CONFIG.AED_PER_EUR).toLocaleString('en-GB')}`;
