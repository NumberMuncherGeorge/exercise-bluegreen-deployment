{{/*
Expand the name of the chart.
*/}}
{{- define "th3-server.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "th3-server.fullname" -}}
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

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "th3-server.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "th3-server.labels" -}}
helm.sh/chart: {{ include "th3-server.chart" . }}
{{ include "th3-server.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
General Selector labels
*/}}
{{- define "th3-server.selectorLabels" -}}
app.kubernetes.io/name: {{ include "th3-server.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Deployment Selector labels
*/}}
{{- define "th3-server.deploymentSelectorLabels" -}}
app.kubernetes.io/version: {{ .tag }}
app.kubernetes.io/deployment: {{ .id }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "th3-server.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "th3-server.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
