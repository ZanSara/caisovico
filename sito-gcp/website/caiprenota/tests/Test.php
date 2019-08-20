<?php
	/**
	* Abstract class representing a generic test.
	* To create a test, extend this class and create any number
	* of test methods, then instantiate that class and invoke the run() method.
	* Tests are considered failed if they throw any exception.
	* during their execution.
	* The class makes available to its children various assert methods.
	* All assert methods throw an exception if their condition has not been met.
	*/
	abstract class Test {
		private $testCount;
		private $testName;
		private $failedTests;
		private $passedTests;
		protected $mysqli;
		const TEST_DB = "my_tre3qwerty_test";

		/**
		* Construct a new test with the given name.
		* This method initializes a protected mysqli object,
		* enabling any child class to quickly access the Database.
		* @param string $testName Name of the test. Can be empty.	
		*/
		public function __construct($testName) {
			$this->testCount = 0;
			$this->testName = $testName;
			$this->failedTests = 0;
			$this->passedTests = 0;
			$this->mysqli = new mysqli("localhost", "root", "", Test::TEST_DB);
			if($this->mysqli->connect_error != NULL) {
				die("An unexpected error has occured while establishing a DB connection: " . $this->mysqli->connect_error);
			}

			$this->mysqli->set_charset("utf8");
		}

		/**
		* Method executed before every test method.
		* It has no base implementation, as it is intended
		* to be overridden in a child class if needed.
		*/
		public function before(){}

		/**
		* Method executed after every test method.
		* It has no base implementation, as it is intended
		* to be overridden in a child class if needed.
		*/
		public function after(){}
		/**
		* Method executed before the first test method.
		* It has no base implementation, as it is intended
		* to be overridden in a child class if needed.
		*/
		public function beforeAll(){}

		/**
		* Method executed after the last test method.
		* It has no base implementation, as it is intended
		* to be overridden in a child class if needed.
		*/
		public function afterAll(){}

		/**
		* Run all tests defined in the class and print messages
		* comunicating the failure and/or success of every test.
		* After all tests have been executed, print global test 
		* stats (total number of passed/failed tests)
		* A test is any method whose name ends with Test
		* All methods will be called with no parameters.
		*/
		public function run() {
			$this->printMessage("Executing test {$this->testName}");
			
			$methods = get_class_methods($this);
			$this->beforeAll();
			foreach ($methods as $method) {
				if(preg_match("/^.*Test$/", $method)) {
					$this->before();
					try {
						$this->{$method}();
						$this->passedTests++;
						echo "<span style='color: green;'>Test {$method} passed!</span><br>";
					}catch(Exception $e){
						$this->failedTests++;
						echo "<span style='color: red;'>Test {$method} failed!</span><br>";
					}
					$this->after();
				}
			}
			$this->afterAll();

			$this->printMessage("Test {$this->testName} complete ({$this->passedTests} passed; {$this->failedTests} failed)");
		}

		/**
		* Print a message in the following format:
		* ===========
		* = Content =
		* ===========
		* The message is printed with a monospaced font.
		*
		* @param string $content The content of the message
		*/
		private function printMessage($content) {
			$border = "";

			for($i = 0; $i < strlen($content) + 4; $i++) {
				$border .= "=";
			}

			echo $border . "<br>= " . $content . " =<br>" . $border . "<br>";
		}

		/**
		* Checks if the given statement is true.
		* Note that this method checks for equality
		* to true, not identity. Hence, assertTrue(1),
		* assertTrue(true), assertTrue("test") are all
		* valid calls to the method.
		* 
		* @param mixed $statement The statement to check
		* @throws Exception if the statement is not true
		*/
		protected function assertTrue($statement) {
			if(!$statement) {
				echo "Expected true, was false<br>";
				throw new Exception("Assert failed", 1);
			}
		}

		/**
		* Checks if the given statement is false.
		* Note that this method checks for equality
		* to false, not identity. Hence, assertFalse(0),
		* assertFalse(false), assertFalse("") are all
		* valid calls to the method.
		* 
		* @param mixed $statement The statement to check
		* @throws Exception if the statement is true
		*/
		protected function assertFalse($statement) {
			if($statement) {
				echo "Expected false, was true";
				throw new Exception("Assert failed", 1);
			}
		}

		/**
		* Checks for equality between the given values.
		* Note that this method checks for identity between
		* the values, so assertEquals("1", 1) and similar will
		* fail the assertion.
		*
		* @param mixed $val1 First value to check
		* @param mixed $val2 Second value to check
		* @throws Exception if the values are not identical
		*/
		protected function assertEquals($val1, $val2) {
			if($val1 !== $val2) {
				echo "Expected {$val1} === {$val2}, values were not identical";
				throw new Exception("Assert failed", 1);
			}
		}

		/**
		* Checks for inequality between the given values.
		* Note that this method checks that the values are not identical,
		* so assertEquals("1", 1) and similar will fulfill the assertion.
		*
		* @param mixed $val1 First value to check
		* @param mixed $val2 Second value to check
		* @throws Exception if the values are identical
		*/
		protected function assertNotEquals($val1, $val2) {
			if($val1 === $val2) {
				echo "Expected {$val1} !== {$val2}, values were identical";
				throw new Exception("Assert failed", 1);
			}
		}

		/**
		* Cleanup method for the Test.
		* Closes the mysqli connection.
		*/
		public function __destruct() {
			$this->mysqli->close();
		}
	}
?>