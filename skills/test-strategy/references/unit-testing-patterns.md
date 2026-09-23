# Patterns de Tests Unitaires par Framework

## Table des matières
1. JavaScript/TypeScript (Jest / Vitest)
2. Python (Pytest)
3. Java (JUnit 5 + Mockito)
4. Swift (XCTest)

---

## 1. JavaScript / TypeScript — Jest & Vitest

### Setup de base

```typescript
// jest.config.ts / vitest.config.ts
export default {
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 }
  }
};
```

### Mocking de dépendances

```typescript
// Mock d'un module entier
jest.mock('./database');
// ou avec Vitest
vi.mock('./database');

// Mock d'une fonction spécifique
const mockSave = jest.fn().mockResolvedValue({ id: 1 });

// Mock avec implémentation
jest.mock('./emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue(true)
}));
```

### Pattern AAA complet

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should_create_user_when_all_fields_are_valid', async () => {
      // Arrange
      const mockRepo = { save: jest.fn().mockResolvedValue({ id: 1, name: 'Alice' }) };
      const service = new UserService(mockRepo);
      const input = { name: 'Alice', email: 'alice@test.com' };

      // Act
      const result = await service.createUser(input);

      // Assert
      expect(result).toEqual({ id: 1, name: 'Alice' });
      expect(mockRepo.save).toHaveBeenCalledWith(input);
      expect(mockRepo.save).toHaveBeenCalledTimes(1);
    });

    it('should_throw_validation_error_when_email_is_empty', async () => {
      // Arrange
      const mockRepo = { save: jest.fn() };
      const service = new UserService(mockRepo);

      // Act & Assert
      await expect(service.createUser({ name: 'Alice', email: '' }))
        .rejects.toThrow('Email is required');
      expect(mockRepo.save).not.toHaveBeenCalled();
    });
  });
});
```

### Tester les cas limites courants

```typescript
// Null / undefined
it('should_return_null_when_user_not_found', ...);

// Chaînes vides
it('should_throw_when_name_is_empty_string', ...);

// Limites numériques
it('should_reject_negative_quantities', ...);
it('should_handle_max_integer_value', ...);

// Tableaux
it('should_return_empty_array_when_no_results', ...);
it('should_handle_single_element_array', ...);

// Async / erreurs
it('should_throw_timeout_when_api_is_slow', ...);
it('should_retry_on_transient_failure', ...);
```

---

## 2. Python — Pytest

### Fixtures et injection

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.get_user = AsyncMock(return_value={"id": 1, "name": "Alice"})
    return db

@pytest.fixture
def user_service(mock_db):
    return UserService(db=mock_db)
```

### Pattern AAA

```python
class TestUserService:
    async def test_should_return_user_when_id_exists(self, user_service, mock_db):
        # Arrange
        user_id = 1

        # Act
        result = await user_service.get_user(user_id)

        # Assert
        assert result == {"id": 1, "name": "Alice"}
        mock_db.get_user.assert_called_once_with(user_id)

    async def test_should_raise_not_found_when_id_invalid(self, user_service, mock_db):
        # Arrange
        mock_db.get_user = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await user_service.get_user(999)
```

### Paramétrage pour les cas limites

```python
@pytest.mark.parametrize("email,expected_valid", [
    ("user@example.com", True),
    ("", False),
    ("no-at-sign", False),
    ("user@.com", False),
    ("a" * 255 + "@test.com", False),
])
def test_should_validate_email_format(email, expected_valid):
    assert validate_email(email) == expected_valid
```

---

## 3. Java — JUnit 5 + Mockito

### Setup

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;
```

### Pattern AAA

```java
    @Test
    @DisplayName("should create user when all fields are valid")
    void should_create_user_when_all_fields_are_valid() {
        // Arrange
        var input = new CreateUserRequest("Alice", "alice@test.com");
        var expected = new User(1L, "Alice", "alice@test.com");
        when(userRepository.save(any())).thenReturn(expected);

        // Act
        var result = userService.createUser(input);

        // Assert
        assertThat(result).isEqualTo(expected);
        verify(userRepository, times(1)).save(any());
    }

    @Test
    @DisplayName("should throw when email is null")
    void should_throw_when_email_is_null() {
        // Arrange
        var input = new CreateUserRequest("Alice", null);

        // Act & Assert
        assertThrows(ValidationException.class,
            () -> userService.createUser(input));
        verifyNoInteractions(userRepository);
    }
```

---

## 4. Swift — XCTest

### Pattern AAA

```swift
final class UserServiceTests: XCTestCase {
    private var sut: UserService!
    private var mockRepository: MockUserRepository!

    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        sut = UserService(repository: mockRepository)
    }

    func test_should_return_user_when_id_exists() async throws {
        // Arrange
        let expectedUser = User(id: 1, name: "Alice")
        mockRepository.stubbedUser = expectedUser

        // Act
        let result = try await sut.getUser(id: 1)

        // Assert
        XCTAssertEqual(result, expectedUser)
        XCTAssertEqual(mockRepository.getCallCount, 1)
    }

    func test_should_throw_when_user_not_found() async {
        // Arrange
        mockRepository.stubbedUser = nil

        // Act & Assert
        do {
            _ = try await sut.getUser(id: 999)
            XCTFail("Expected UserNotFoundError")
        } catch {
            XCTAssertTrue(error is UserNotFoundError)
        }
    }
}
```
