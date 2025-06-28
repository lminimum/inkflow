export interface NavigationItem {
  to?: string
  icon?: any
  label?: string
  handler?: () => void
}

export interface Model {
  id: string;
  object: string;
  created: number;
  owned_by: string;
}

export interface ModelListResponse {
  object: string;
  data: Model[];
}