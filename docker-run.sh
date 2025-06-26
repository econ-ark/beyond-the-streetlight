#!/bin/bash

# Beyond the Streetlight - Docker Management Script
# This script provides easy commands for building and running the Docker container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show usage
usage() {
    echo "Beyond the Streetlight - Docker Management"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build          Build the Docker image"
    echo "  reproduce      Run full reproduction workflow"
    echo "  analysis       Run analysis workflow only"
    echo "  jupyter        Start Jupyter Lab server"
    echo "  shell          Start interactive shell"
    echo "  clean          Remove containers and images"
    echo "  help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build          # Build the image"
    echo "  $0 reproduce      # Run full analysis"
    echo "  $0 jupyter        # Start Jupyter on http://localhost:8888"
    echo ""
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t beyond-the-streetlight:latest .
    print_success "Docker image built successfully!"
}

# Run reproduction
run_reproduce() {
    print_status "Running full reproduction workflow..."
    docker-compose run --rm reproduce
    print_success "Reproduction completed!"
}

# Run analysis only
run_analysis() {
    print_status "Running analysis workflow..."
    docker-compose run --rm analysis
    print_success "Analysis completed!"
}

# Start Jupyter Lab
start_jupyter() {
    print_status "Starting Jupyter Lab..."
    print_warning "Jupyter Lab will be available at: http://localhost:8888"
    docker-compose up jupyter
}

# Start interactive shell
start_shell() {
    print_status "Starting interactive shell..."
    docker-compose run --rm shell
}

# Clean up containers and images
clean_docker() {
    print_status "Cleaning up Docker containers and images..."
    
    # Stop and remove containers
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove the image
    docker rmi beyond-the-streetlight:latest 2>/dev/null || true
    
    print_success "Docker cleanup completed!"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Main script logic
main() {
    # Check if Docker is available
    check_docker
    
    case "${1:-help}" in
        build)
            build_image
            ;;
        reproduce)
            build_image
            run_reproduce
            ;;
        analysis)
            build_image
            run_analysis
            ;;
        jupyter)
            build_image
            start_jupyter
            ;;
        shell)
            build_image
            start_shell
            ;;
        clean)
            clean_docker
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 