/**
 * @file common.js
 * @date 2025-02-14
 * @author Bryan Gillis
 */


/**
 * Gets whether or not the app is operating in "Service mode"
 * 
 * This is the mode used for the public web app.
 *
 * @return {bool} True indicates service mode, False indicates local mode
 */
export function getServiceMode() {
  return sessionStorage.getItem("service_mode");
}

/**
 * Sets the service mode for the CSS document of the current page
 */
export function loadServiceMode() {
  document.documentElement.setAttribute("service-mode", getServiceMode());
}

/**
 * Gets whether or not the app is operating in "Production mode"
 * 
 * This is the mode used in staging/production deployments, but not dev deployments
 *
 * @return {bool} True indicates production mode, False indicates dev mode
 */
export function getProductionMode() {
  return sessionStorage.getItem("production_mode");
}

/**
 * Sets the production mode for the CSS document of the current page
 */
export function loadProductionMode() {
  document.documentElement.setAttribute("production-mode", getProductionMode());
}