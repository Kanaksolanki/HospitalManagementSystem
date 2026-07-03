// Signature element: an ECG-style trace used as a section divider throughout
// the app. Doubles as a subtle "live" indicator — active state (green stroke)
// signals a page with real-time-ish data (queues, upcoming appointments).
export default function PulseDivider({ active = false }) {
  return (
    <svg
      className={`pulse-divider${active ? " active" : ""}`}
      viewBox="0 0 400 24"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <path d="M0,12 L140,12 L152,2 L164,22 L176,12 L400,12" />
    </svg>
  );
}