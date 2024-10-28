name: Deploy to Azure Web App

on:
  workflow_dispatch:
  push:
    branches:
      - main  # Ensure you are on the main branch when you push changes

env:
  AZURE_WEBAPP_NAME: cxqa-webapp  # The name of your Azure Web App
  AZURE_WEBAPP_PACKAGE_PATH: "./publish"  # Path for deployment package

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Create package directory
        run: mkdir -p ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}

      - name: Copy files to package directory
        run: cp -r * ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}

      - name: Package for deployment
        run: zip -r ${AZURE_WEBAPP_PACKAGE_PATH}.zip ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}/*

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}  # Ensure this is set correctly
          package: "${{ env.AZURE_WEBAPP_PACKAGE_PATH }}.zip"
