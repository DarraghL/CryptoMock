def test_services():
    """Test that services are properly initialized"""
    from app.services import price_service, trading_service
    
    # Test price service
    assert price_service is not None
    assert hasattr(price_service, 'get_price')
    
    # Test trading service
    assert trading_service is not None
    assert hasattr(trading_service, 'execute_buy')
    assert hasattr(trading_service, 'execute_sell')

if __name__ == "__main__":
    from app import create_app
    
    app = create_app()
    with app.app_context():
        test_services()
        print("Services initialized successfully!")