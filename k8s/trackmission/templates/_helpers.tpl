{{- define "trackmission.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "trackmission.db.fullname" -}}
{{- $name := .Chart.Name }}
{{- if contains $name .Release.Name }}
{{- printf "%s-%s" "db" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s-%s" "db" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "trackmission.labels" -}}
{{ include "trackmission.selectorLabels" .}}
app.kubernetes.io/version: "{{ .Values.image.tag | default .Chart.AppVersion }}"
app.kubernetes.io/managed-by: helm
{{- end -}}

{{- define "trackmission.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
release: {{ .Release.Name }}
{{- end -}}

{{- define "db.selectorLabels" -}}
app: db
{{- end -}}
