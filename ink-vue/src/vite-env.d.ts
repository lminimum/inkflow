declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
declare module '*.css' {
  const classes: { [key: string]: string }
  export default classes
}
