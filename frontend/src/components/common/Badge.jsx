const VARIANT_CLASS = {
  primary: "badge-primary",
  success: "badge-success",
  danger: "badge-danger",
  accent: "badge-accent",
  neutral: "badge-neutral",
};

export default function Badge({ variant = "neutral", children }) {
  return <span className={`badge ${VARIANT_CLASS[variant] || VARIANT_CLASS.neutral}`}>{children}</span>;
}