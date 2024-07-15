resource "kubernetes_namespace" "ingress" {
  count = local.is_default_workspace ? 0 : 1
  metadata {
    name = "ingress"
  }
}

resource "helm_release" "ingress" {
  count      = local.is_default_workspace ? 0 : 1
  name       = "ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.7.5"
  namespace  = kubernetes_namespace.ingress[0].metadata.0.name
  depends_on = [
    kubernetes_namespace.ingress[0]
  ]
}
